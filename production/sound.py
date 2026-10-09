"""Seeded local motion Foley, scored from word-anchored events with waveform ducking."""
import argparse,json,math
import numpy as np
import soundfile as sf
from core import ROOT,paths,read,write,sha,export

def synth(name,frames,rate=48000):
    n=frames*1600;t=np.arange(n)/rate;p=np.arange(n)/max(1,n-1)
    rng=np.random.default_rng(42+sum(map(ord,name)))
    noise=rng.standard_normal(n)
    low=np.convolve(noise,np.ones(41)/41,mode='same')
    air=noise-np.convolve(noise,np.ones(7)/7,mode='same')
    env=np.minimum(1,t/.008)*np.minimum(1,(n/rate-t)/.12)
    chirp=lambda a,b:np.sin(2*np.pi*(a*t+(b-a)*t*t/(2*n/rate)))
    if name in ['tick','latch']:
        x=(chirp(1450,600)*.35+air*.2+chirp(180,90)*.45)*np.exp(-t*(45 if name=='tick' else 15))
        if name=='latch':x+=np.roll(x,round(rate*.04))*.4
    elif name in ['paper','fold','swish']:
        x=low*2.5*np.sin(np.pi*p)**1.4+air*.035
        if name!='swish':x+=chirp(700,190)*np.exp(-((p-.35)/.045)**2)*.17
        if name=='fold':x+=chirp(180,65)*np.exp(-p*4)*.4
    elif name in ['scale','coil','riser']:
        a,b=(65,180) if name=='riser' else (210,48)
        x=(chirp(a,b)*.4+chirp(a*2.03,b*2.03)*.17+low*.75)*np.sin(np.pi*p)**.8
        x+=air*.07*np.sin(np.pi*p)**2
    elif name=='ratchet':
        x=np.zeros(n)
        for pulse in np.linspace(.04,.9,8)**.7:
            dt=t-pulse*n/rate
            x+=(chirp(1100,700)*.3+air*.18)*np.exp(-np.maximum(0,dt)*80)*(dt>=0)
    else:
        x=(chirp(210,105)*.48+chirp(420,280)*.22+low*.3)*np.exp(-p*(5 if name=='impact' else 3))
        if name=='impact':x+=chirp(65,45)*np.exp(-p*5)*.28
    x*=env
    return x/max(.01,float(np.max(np.abs(x))))*.72

def build(id, speech_ratio=.27, master_gain=.3):
    _,dest=paths(id);m=read(dest/'narration-manifest.json');d=read(dest/'word-timings.json')
    if not m.get('direction'):raise ValueError('Author a word-anchored storyboard first')
    voice,rate=sf.read(dest/'narration.wav');assert rate==48000
    n=m['timeline']['outroFromFrame']*1600
    stem=np.zeros(n);events=[]
    for event in m['direction']['events']:
        for i,e in enumerate(event['effects']):
            wave=synth(e['sound'],e['durationFrames'])*e['gain']*master_gain
            start=e['frame']*1600;stop=start+len(wave)
            if stop>n:raise ValueError('Effect overlaps outro')
            stem[start:stop]+=wave
            events.append({**e,'event':event['id'],'id':f"{event['id']}-{i}"})
    # Actual imported waveform controls the sidechain. No guessed talking cadence.
    v=np.pad(voice*.9,(0,n-len(voice)))
    windows=int(math.ceil(n/480))
    vrms=np.array([np.sqrt(np.mean(v[i*480:(i+1)*480]**2)) for i in range(windows)])
    srms=np.array([np.sqrt(np.mean(stem[i*480:(i+1)*480]**2)) for i in range(windows)])
    speech=vrms>.008
    # Look ahead30ms, release140ms; keep effects ~11dB below speech in active windows.
    target=np.ones(windows)
    for i in range(windows):
        level=vrms[i]
        if level>.008:target[i]=min(1,level*speech_ratio/max(srms[i],1e-6))
    target=np.array([min(target[max(0,i-1):min(windows,i+4)]) for i in range(windows)])
    gain=np.ones(windows)
    for i in range(1,windows):gain[i]=min(target[i],gain[i-1]+1/14)
    envelope=np.interp(np.arange(n),np.arange(windows)*480+240,gain)
    stem*=envelope
    peak=float(np.max(np.abs(stem+v)))
    if peak>.85:stem*=.85/peak
    # Preserve the protected EpisodeComposition's existing0.6 SFX gain.
    sf.write(dest/'sfx-stem.wav',stem/.6,48000,subtype='PCM_24')
    srms_after=np.array([np.sqrt(np.mean(stem[i*480:(i+1)*480]**2)) for i in range(windows)])
    voiced=speech & (srms_after>.0003)
    ratios=20*np.log10(np.maximum(srms_after[voiced],1e-9)/vrms[voiced])
    report={'schemaVersion':1,'method':'original-seeded-procedural-foley-v2','seed':42,'sampleRate':48000,'directionHash':sha(json.dumps(m['direction'],sort_keys=True).encode()),'audioHash':d['bindings']['audioHash'],'stemSha256':sha((dest/'sfx-stem.wav').read_bytes()),'events':events,'ducking':{'source':'actual narration WAV, 10ms RMS','speechRatioLimit':speech_ratio,'masterGain':master_gain,'lookaheadMs':30,'releaseMs':140,'minimumGain':float(gain.min()),'speechWindowsWithSfx':int(voiced.sum()),'medianEffectToVoiceDb':float(np.median(ratios)) if len(ratios) else None,'p95EffectToVoiceDb':float(np.percentile(ratios,95)) if len(ratios) else None},'stemPeak':float(np.max(np.abs(stem))),'predictedMixPeak':float(np.max(np.abs(stem+v))),'externalSamples':False,'humanListeningPerformed':False}
    report['renderGain']=.6
    write(dest/'sound-design.json',report)
    export(id)
    print(json.dumps({k:report[k] for k in ['ducking','stemPeak','predictedMixPeak']},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--id',required=True);a=p.parse_args();build(a.id)
