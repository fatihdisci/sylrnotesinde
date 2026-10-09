"""Validate the actual encoded mobile comparison and extract real MP4 review frames."""
import array, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
if sys.prefix==sys.base_prefix:
    raise SystemExit(subprocess.call([str(ROOT/'environments/antalia-mini/bin/python'),__file__]))
import numpy as np
import soundfile as sf

def main():
    manifest=json.loads((ROOT/'comparison/reel-manifest.json').read_text())
    video=ROOT.parent/'renders/tts-12-profiles.mp4'
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)]))
    stream=next(s for s in probe['streams'] if s['codec_type']=='video')
    assert (stream['width'],stream['height'],stream['r_frame_rate'],int(stream['nb_read_frames']))==(1080,1920,'30/1',manifest['durationInFrames'])
    data=subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-map','0:a:0','-ac','1','-ar','48000','-f','f32le','-'])
    encoded=np.frombuffer(data,dtype='<f4')
    assert np.isfinite(encoded).all() and float(np.max(np.abs(encoded)))<.99
    checks=[]
    for clip in manifest['clips']:
        source,rate=sf.read(ROOT.parent/'public'/clip['audio'],dtype='float32')
        assert rate==48000 and len(source)>rate
        metadata=json.loads((ROOT/'outputs/mobile-reel'/clip['model']/clip['voice']/'sentence.json').read_text())
        assert metadata['text']==manifest['text'] and metadata['networkAttempts']==[]
        start=(clip['fromFrame']+6)*1600
        # FFmpeg's millisecond audio-delay rounding can move a clip by <1 ms.
        # Locate the decoded waveform, then validate both identity and measured offset.
        margin=96
        window=encoded[start-margin:start+len(source)+margin]
        fft_size=1 << (len(window)+len(source)-2).bit_length()
        convolution=np.fft.irfft(np.fft.rfft(window,fft_size)*np.fft.rfft(source[::-1],fft_size),fft_size)
        offset=int(np.argmax(convolution[len(source)-1:len(source)+2*margin]))
        target=window[offset:offset+len(source)]
        lag=offset-margin
        corr=float(np.corrcoef(source,target)[0,1])
        assert corr>.95 and abs(lag)<=48, (clip['name'],clip['voice'],corr,lag)
        checks.append(dict(model=clip['name'],voice=clip['voice'],seconds=len(source)/rate,aacCorrelation=corr,encodedOffsetSamples=lag,startsAtSeconds=(clip['fromFrame']+6)/30))
    review=ROOT.parent/'renders/voice-comparison-review';review.mkdir(exist_ok=True)
    frames=[manifest['clips'][i]['fromFrame']+30 for i in [0,1,2,6,7,11]]
    select='+'.join(f'eq(n,{f})' for f in frames)
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(video),'-vf',f"select='{select}',scale=360:640,tile=3x2",'-frames:v','1',str(review/'actual-mp4-contact-sheet.png')],check=True)
    result=dict(profiles=checks,width=1080,height=1920,fps=30,frames=manifest['durationInFrames'],seconds=manifest['durationInFrames']/30,encodedPeak=float(np.max(np.abs(encoded))),fileBytes=video.stat().st_size,reviewFrames=frames,subjectiveListeningPerformed=False)
    (ROOT/'comparison/reel-qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(f'PASS: twelve matching voice segments in actual AAC track, {result["seconds"]:.2f}s, {result["fileBytes"]/1024**2:.2f} MiB.')
if __name__=='__main__':main()
