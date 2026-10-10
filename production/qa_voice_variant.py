"""Measure the experimental MP4 against its processed voice and unchanged stems."""
import argparse, hashlib, json, subprocess
from pathlib import Path
import numpy as np
import soundfile as sf
from qa import correlate, pcm
from voice_variant import ROOT, RATE

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--video', type=Path, required=True)
    args=parser.parse_args();video=args.video.resolve()
    read=lambda p:json.loads(p.read_text())
    report=read(video.with_suffix('.json'))
    assets=ROOT/'public/episodes/solar-basketball'
    work=ROOT/'renders/experiments/solar-basketball-voice-minus-half'
    manifest=read(assets/'narration-manifest.json');words=read(assets/'word-timings.json')
    source_video=ROOT/report['sourceVideo']
    assert hashlib.sha256(source_video.read_bytes()).hexdigest()==report['sourceVideoSha256']
    assert hashlib.sha256(video.read_bytes()).hexdigest()==report['videoSha256']
    for file,key in [('narration.wav','sourceNarrationSha256'),('sfx-stem.wav','sfxStemSha256'),('ambient-stem.wav','musicStemSha256')]:
        assert hashlib.sha256((assets/file).read_bytes()).hexdigest()==report[key]
    picture_hash=lambda p:subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:v:0','-c:v','copy','-f','hash','-hash','sha256','-'],text=True).strip()
    assert picture_hash(video)==picture_hash(source_video)
    probe=read_probe(video);stream=next(s for s in probe['streams'] if s['codec_type']=='video')
    assert (stream['width'],stream['height'],stream['r_frame_rate'],int(stream['nb_read_frames']))==(1080,1920,'30/1',manifest['durationInFrames'])
    encoded=pcm(video);mix=pcm(work/'mix-minus-half-eq.wav');treated=pcm(work/'narration-minus-half-eq.wav')
    original=pcm(assets/'narration.wav');assert len(treated)==len(original)
    assert np.isfinite(encoded).all() and np.max(np.abs(encoded))<.99
    start=manifest['narration'][0]['from']*1600
    accompaniment=mix.copy();accompaniment[start:start+len(treated)]-=treated*report['mixLevels']['narration']
    isolated=encoded[:len(accompaniment)]-accompaniment
    # FFmpeg stereo->mono diagnostics undo the equal-power channel split.
    gain=report['mixLevels']['narration']
    original_encoded=pcm(source_video)[:len(accompaniment)]-accompaniment
    old_gain=float(np.dot(original,original_encoded[start:start+len(original)])/np.dot(original,original))
    new_gain=float(np.dot(treated,isolated[start:start+len(treated)])/np.dot(treated,treated))
    assert abs(old_gain-gain)<.005 and abs(new_gain-gain)<.005,(old_gain,new_gain,gain)
    checks=[]
    for label,index in [('start',0),('middle',len(words['words'])//2),('end',len(words['words'])-3)]:
        a=max(0,round(words['words'][index]['startMs']*48)-3840);b=min(len(treated),a+48000)
        lag,corr=correlate(treated[a:b]*report['mixLevels']['narration'],isolated,start+a)
        assert abs(lag)<=1000/30 and corr>.95,(label,lag,corr)
        checks.append({'position':label,'lagMs':lag,'correlation':corr})
    mix_checks=[]
    for event in manifest['direction']['events']:
        a=event['from']*1600;b=min(len(mix),a+24000)
        if b-a<4800:continue
        lag,corr=correlate(mix[a:b],encoded,a)
        assert abs(lag)<=1000/30 and corr>.98,(event['id'],lag,corr)
        mix_checks.append({'event':event['id'],'lagMs':lag,'correlation':corr})
    # Compare slow energy envelopes to detect processing-induced phrase drift.
    # This is not a phoneme-level or human word-timing approval.
    envelope=lambda x:np.convolve(np.sqrt(np.mean(x[:len(x)//240*240].reshape(-1,240)**2,axis=1)),np.ones(8)/8,mode='same')
    old,new=envelope(original),envelope(treated);envelope_checks=[]
    for label,at in [('start',0),('middle',27),('end',55)]:
        a=at*200;b=min(len(old),a+8*200)
        candidates=[]
        for shift in range(-20,21):
            lo=max(a,-shift);hi=min(b,len(new)-shift)
            corr=float(np.corrcoef(old[lo:hi],new[lo+shift:hi+shift])[0,1])
            candidates.append((corr,shift*5))
        corr,lag=max(candidates);assert abs(lag)<=1000/30 and corr>.9,(label,lag,corr)
        envelope_checks.append({'position':label,'lagMs':lag,'correlation':corr})
    outro=manifest['timeline']['outroFromFrame']*1600
    closing=pcm(ROOT/'public/audio/brand/closing.wav');lag,corr=correlate(closing,encoded,outro)
    assert abs(lag)<=1000/30 and corr>.95
    analysis=subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-af','loudnorm=I=-20:TP=-2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    loud=json.loads(analysis.stderr[analysis.stderr.rfind('{'):analysis.stderr.rfind('}')+1])
    assert float(loud['input_tp'])<=-1
    result={'variantChecksPassed':True,'videoSha256':report['videoSha256'],
        'pictureStreamIdentical':True,'sourceDeliveryUnchanged':True,
        'expectedNarrationMonoDecodeGain':gain,'sourceMeasuredNarrationMonoDecodeGain':old_gain,
        'variantMeasuredNarrationMonoDecodeGain':new_gain,
        'frames':int(stream['nb_read_frames']),'fps':30,'width':1080,'height':1920,
        'voiceEncodedSync':checks,'fullMixEncodedSync':mix_checks,
        'processingEnvelopeSync':envelope_checks,
        'processingEnvelopeResolutionMs':5,'processingEnvelopeSmoothingMs':40,'outroLagMs':lag,'outroCorrelation':corr,
        'integratedLufs':float(loud['input_i']),'truePeakDbtp':float(loud['input_tp']),
        'generalLoudnessPolicyPassed':-25<=float(loud['input_i'])<=-17,
        'humanListeningPerformed':False,'wordTimingManuallyApproved':False,
        'publicationReady':False,
        'limitations':['Envelope alignment is a phrase-level diagnostic, not one-frame word accuracy.',
          'Listen for pitch/EQ artifacts and Turkish consonant clarity.',
          'Existing caption human review remains pending.',
          'Quiet user-selected mix is measured without changing the general loudness policy.']}
    video.with_suffix('.qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

def read_probe(video):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(video)]))

if __name__=='__main__':main()
