"""Checks the encoded output, extracts actual MP4 frames, writes a contact sheet."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops, ImageStat
import subprocess
import json
import array
import math
import wave

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'renders' / 'qa'
OUT.mkdir(parents=True, exist_ok=True)

def run(args):
    return subprocess.check_output(args)

report = {'video': {}, 'audio': {}, 'temporal': {}}
decoded_audio = {}
for name, frames in [('style-proof', 450), ('outro', 45)]:
    path = ROOT / 'renders' / f'{name}.mp4'
    data = json.loads(run(['ffprobe', '-v', 'error', '-count_frames', '-show_streams', '-show_format', '-of', 'json', str(path)]))
    v = next(s for s in data['streams'] if s['codec_type'] == 'video')
    assert (v['width'], v['height'], v['r_frame_rate'], int(v['nb_read_frames'])) == (1080, 1920, '30/1', frames)
    assert abs(float(v['duration']) - frames / 30) < 0.001
    assert v['codec_name'] == 'h264' and v['pix_fmt'] == 'yuv420p'
    report['video'][name] = {k: v[k] for k in ['width', 'height', 'r_frame_rate', 'duration', 'nb_read_frames', 'codec_name', 'pix_fmt']}
    pcm = array.array('f', run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'f32le', '-ar', '48000', '-ac', '1', '-']))
    decoded_audio[name] = pcm
    peak = max(map(abs, pcm))
    assert peak < 0.98, f'{name} clipping'
    tail = pcm[round((frames/30 - 0.12)*48000):round(frames/30*48000)]
    rms = math.sqrt(sum(v*v for v in tail) / len(tail))
    assert rms < 0.001, 'Audio tail has not decayed before end'
    report['audio'][name] = {'decodedPeakDBFS': round(20*math.log10(peak), 2),
                             'last120msRMS': rms, 'encodedSamples': len(pcm),
                             'note': 'AAC encoder padding may extend audio stream; video has exact frame count.'}
    # Decode every frame at quarter size. Minimum detail rejects a blank frame;
    # mean absolute inter-frame difference is reported, not called proof of smoothness.
    width, height = 270, 480
    process = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(path), '-vf', f'scale={width}:{height}',
                                '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    previous, diffs, detail = None, [], []
    background = Image.new('RGB', (width, height), '#111615')
    while True:
        raw = process.stdout.read(width * height * 3)
        if not raw:
            break
        assert len(raw) == width * height * 3
        image = Image.frombytes('RGB', (width, height), raw)
        delta = ImageChops.difference(image, background).convert('L')
        histogram = delta.histogram()
        detail.append(sum(histogram[15:]))
        if previous is not None:
            diffs.append(sum(ImageStat.Stat(ImageChops.difference(image, previous)).mean) / 3)
        previous = image
    assert process.wait() == 0 and len(detail) == frames
    assert min(detail) >= 5, f'Blank frame in {name}'
    report['temporal'][name] = {'decodedFrames': len(detail), 'minimumNonBackgroundPixelsAtQuarterSize': min(detail),
                              'maximumMeanFrameDifference': max(diffs),
                              'largestChanges': sorted(enumerate(diffs, 1), key=lambda p: p[1], reverse=True)[:8]}
    if name == 'style-proof':
        hold_difference = max(diffs[359:404])
        assert hold_difference < 0.5, 'Unintended motion/flash in final hold'
        report['temporal'][name]['finalHoldMaximumMeanDifference'] = hold_difference

# Compare the actual AAC-decoded closing motif in both delivered MP4s.
embedded = decoded_audio['style-proof'][648000:720000]
standalone = decoded_audio['outro'][:72000]
correlation = sum(a*b for a, b in zip(embedded, standalone)) / math.sqrt(sum(a*a for a in embedded)*sum(b*b for b in standalone))
assert correlation > 0.98, 'Embedded and standalone outro motifs differ'
report['audio']['outroIdentity'] = {'decodedCorrelation': correlation}
for onset in [2/30, 10/30, 22/30]:
    begin = round((onset-0.015)*48000)
    end = round((onset+0.12)*48000)
    active = next(i for i in range(begin, end) if abs(standalone[i]) > 0.003) / 48000
    assert abs(active-onset) < 0.025, 'Closing event onset drift'
    report['audio'].setdefault('closingEvents', []).append({'expected': onset, 'decodedActiveStart': active})

voice = json.loads((ROOT / 'public/episodes/style-proof/voice-timing.json').read_text())
for cue in voice:
    with wave.open(str(ROOT / 'public' / cue['path']), 'rb') as f:
        samples = array.array('h', f.readframes(f.getnframes()))
        assert f.getframerate() == 48000
        active = [i for i, s in enumerate(samples) if abs(s) > 32]
        first, last = active[0]/48000, active[-1]/48000
        end = cue['from']/30 + last
        assert end < 13.5
        report['audio'][cue['id']] = {'fileDuration': cue['seconds'], 'timelineStart': cue['from']/30,
                                     'activeStart': cue['from']/30 + first, 'activeEnd': end,
                                     'wordAlignmentVerified': False}

frames = [0, 24, 89, 108, 144, 209, 228, 270, 330, 360, 404, 405, 416, 429, 449]
select = '+'.join(f'eq(n\\,{f})' for f in frames)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(ROOT/'renders/style-proof.mp4'), '-vf', f'select={select}',
                '-fps_mode', 'vfr', str(OUT/'extract-%02d.png')], check=True)
sheet = Image.new('RGB', (324*3, (576+44)*5), '#111615')
draw = ImageDraw.Draw(sheet)
for i, frame in enumerate(frames):
    target = OUT/f'frame-{frame:03d}.png'
    (OUT/f'extract-{i+1:02d}.png').replace(target)
    im = Image.open(target).convert('RGB')
    im.thumbnail((324, 576))
    x, y = (i % 3)*324, (i//3)*620
    sheet.paste(im, (x, y))
    draw.text((x+12, y+586), f'FRAME {frame:03d} / {frame/30:.2f}s', fill='#F2F0E9')
sheet.save(OUT/'contact-sheet.png')
(OUT/'media-report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n')
print(json.dumps(report, indent=2, ensure_ascii=False))
