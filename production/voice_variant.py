"""Create an isolated pitch/EQ listening variant; never rewrite episode assets."""
import argparse, hashlib, json, math, subprocess
from pathlib import Path
import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
RATE = 48000

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--id', default='solar-basketball')
    parser.add_argument('--source-video', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    source_video = args.source_video.resolve()
    output = args.output.resolve()
    if output == source_video or output.exists():
        raise ValueError('Choose a new output path; existing deliveries are protected.')
    assets = ROOT / 'public' / 'episodes' / args.id
    work = ROOT / 'renders' / 'experiments' / (args.id + '-voice-minus-half')
    work.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    load = lambda p: json.loads(p.read_text())
    manifest = load(assets / 'narration-manifest.json')
    score = load(assets / 'sound-design.json')
    voice, rate = sf.read(assets / 'narration.wav')
    assert rate == RATE and voice.ndim == 1
    original_hash = digest(source_video)
    # FFmpeg WSOLA compensates the resampling tempo; no new TTS/model settings.
    shifted_rate = round(RATE * 2 ** (-.5 / 12))
    filters = (f'asetrate={shifted_rate},aresample={RATE},atempo={RATE/shifted_rate:.12f},'
               f'equalizer=f=2800:t=q:w=1:g=-1.5,highpass=f=65,'
               f'apad,atrim=end_sample={len(voice)}')
    treated_path = work / 'narration-minus-half-eq.wav'
    run(['ffmpeg', '-v', 'error', '-y', '-i', str(assets / 'narration.wav'),
         '-af', filters, '-ar', str(RATE), '-c:a', 'pcm_s24le', str(treated_path)])
    treated, rate = sf.read(treated_path)
    assert len(treated) == len(voice) and rate == RATE and np.isfinite(treated).all()
    n = manifest['timeline']['outroFromFrame'] * 1600
    offset = manifest['narration'][0]['from'] * 1600
    mix = np.zeros((n, 2))
    # Match Remotion/FFmpeg's equal-power mono-to-stereo conversion.
    gain = score['narrationRenderGain'] / math.sqrt(2)
    mix[offset:offset+len(treated)] += treated[:, None] * gain
    for file, level in [('sfx-stem.wav', score['renderGain']),
                        (score['musicFile'], score['musicRenderGain'])]:
        stem, sr = sf.read(assets / file)
        assert sr == RATE and stem.ndim == 2 and len(stem) <= n
        mix[:len(stem)] += stem * level
    closing, sr = sf.read(ROOT / 'public/audio/brand/closing.wav')
    assert sr == RATE
    if closing.ndim == 1:
        closing = np.column_stack([closing, closing])
    final = np.concatenate([mix, closing])
    assert np.max(np.abs(final)) < .99
    mix_path = work / 'mix-minus-half-eq.wav'
    sf.write(mix_path, final, RATE, subtype='PCM_24')
    run(['ffmpeg', '-v', 'error', '-n', '-i', str(source_video), '-i', str(mix_path),
         '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac',
         '-b:a', '192k', '-movflags', '+faststart', str(output)])
    assert digest(source_video) == original_hash
    report = {
        'schemaVersion': 1, 'kind': 'isolated-listening-experiment',
        'sourceVideo': str(source_video.relative_to(ROOT)), 'sourceVideoSha256': original_hash,
        'video': str(output.relative_to(ROOT)), 'videoSha256': digest(output),
        'sourceNarrationSha256': digest(assets / 'narration.wav'),
        'processedNarrationSha256': digest(treated_path),
        'voiceProcessing': {'requestedSemitones': -.5,
            'actualSemitones': 12*math.log2(shifted_rate/RATE),
            'method': 'FFmpeg resampling plus WSOLA atempo compensation',
            'formantPreservation': False, 'filters': filters,
            'eq': {'frequencyHz': 2800, 'gainDb': -1.5, 'q': 1},
            'highpassHz': 65, 'sourceSamples': len(voice), 'outputSamples': len(treated)},
        'mixLevels': score['mixLevels'], 'monoToStereoGain': 1/math.sqrt(2), 'musicStemSha256': score['musicStemSha256'],
        'sfxStemSha256': score['stemSha256'], 'outroFromFrame': n//1600,
        'canonicalOutroUnmodified': True, 'humanListeningPerformed': False,
        'publicationReady': False,
        'notes': ['Listening candidate only; not the default narrator.',
                  'Resampling also lowers formants slightly; judge naturalness by listening.',
                  'Exact file length does not prove local word timing; see measured QA.']}
    output.with_suffix('.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(output)

if __name__ == '__main__':
    main()
