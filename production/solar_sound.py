"""Original deterministic stereo film score. Local synthesis; no samples or service."""
import json,math
import numpy as np
import soundfile as sf
from core import ROOT,paths,read,write,sha,export
RATE=48000

def band_noise(n,seed,low,high):
 rng=np.random.default_rng(seed);x=rng.standard_normal(n)
 frequencies=np.fft.rfftfreq(n,1/RATE)
 response=np.minimum(1,(frequencies/max(1,low))**2)*np.minimum(1,(high/np.maximum(1,frequencies))**3)
 response[0]=0
 x=np.fft.irfft(np.fft.rfft(x)*response,n)
 return x/max(1e-9,np.std(x))

def effect(name,frames,seed):
 n=frames*1600;t=np.arange(n)/RATE;p=np.arange(n)/max(1,n-1);duration=n/RATE
 air=band_noise(n,seed,170,3300);low=band_noise(n,seed+1,25,180)
 def sweep(a,b):return np.sin(2*np.pi*(a*t+(b-a)*t*t/(2*duration)))
 if name in ['launch','travel','reveal']:
  env=np.sin(np.pi*p)**1.7
  x=(air*(.18+.32*p)+low*.11+sweep(55,170)*.16+sweep(110,340)*.07)*env
  pan=np.linspace(-.65,.65,n)
 elif name in ['impact','arrival','final','bloom']:
  attack=np.minimum(1,t/.012);env=attack*np.exp(-p*4.4)*np.minimum(1,(1-p)*10)
  x=(sweep(91,37)*.42+sweep(182,74)*.16+sweep(470,240)*.12+air*.08+low*.07)*env
  if name=='bloom':x+=sweep(155,290)*np.sin(np.pi*p)**2*.08
  if name=='final':x+=np.sin(2*np.pi*146.83*t)*np.sin(np.pi*p)**2*.12
  pan=np.sin(p*np.pi)*.12
 elif name=='click':
  x=(sweep(1700,700)*.22+air*.18+sweep(320,140)*.14)*np.exp(-t*24)*np.minimum(1,t/.003)*np.minimum(1,(1-p)*8)
  pan=np.zeros(n)
 else:
  env=np.sin(np.pi*p)**1.4
  x=(air*.16+low*.05+sweep(180,100)*.08)*env
  if name=='leather':x+=sweep(430,170)*np.exp(-((p-.28)/.05)**2)*.2
  pan=np.sin(p*np.pi*2)*.25
 x=x/max(1e-9,np.max(np.abs(x)))*.43
 return np.stack([x*np.sqrt((1-pan)/2),x*np.sqrt((1+pan)/2)],axis=1)

def sidechain(voice,stem,ratio):
 n=len(voice);windows=math.ceil(n/480)
 vrms=np.array([np.sqrt(np.mean(voice[i*480:(i+1)*480]**2)) for i in range(windows)])
 mono=stem.mean(axis=1);srms=np.array([np.sqrt(np.mean(mono[i*480:(i+1)*480]**2)) for i in range(windows)])
 target=np.where(vrms>.008,np.minimum(1,vrms*ratio/np.maximum(srms,1e-8)),1)
 target=np.array([target[max(0,i-1):min(windows,i+4)].min() for i in range(windows)])
 gain=np.ones(windows)
 for i in range(1,windows):gain[i]=min(target[i],gain[i-1]+1/18)
 env=np.interp(np.arange(n),np.arange(windows)*480+240,gain)
 stem*=env[:,None]
 after=np.array([np.sqrt(np.mean(stem[i*480:(i+1)*480].mean(axis=1)**2)) for i in range(windows)])
 voiced=(vrms>.008)&(after>.0001);ratios=20*np.log10(np.maximum(after[voiced],1e-9)/vrms[voiced])
 return stem,{'lookaheadMs':30,'releaseMs':180,'speechRatioLimit':ratio,'minimumGain':float(gain.min()),'medianEffectToVoiceDb':float(np.median(ratios)) if len(ratios) else None,'p95EffectToVoiceDb':float(np.percentile(ratios,95)) if len(ratios) else None,'source':'actual narration WAV 10ms RMS'}

def build(id='solar-basketball'):
 _,dest=paths(id);m=read(dest/'narration-manifest.json');d=read(dest/'word-timings.json')
 voice,rate=sf.read(dest/'narration.wav');assert rate==RATE and voice.ndim==1
 n=m['timeline']['outroFromFrame']*1600;v=np.pad(voice*.9,(0,n-len(voice)))
 sfx=np.zeros((n,2));events=[]
 for event in m['direction']['events']:
  for i,e in enumerate(event['effects']):
   wave=effect(e['sound'],e['durationFrames'],42+e['frame'])*e['gain'];start=e['frame']*1600
   if start+len(wave)>n:raise ValueError('Effect crosses outro')
   sfx[start:start+len(wave)]+=wave;events.append({**e,'event':event['id'],'id':f'{event["id"]}-{i}'})
 sfx,duck=sidechain(v,sfx,.42)
 t=np.arange(n)/RATE;music=np.zeros((n,2))
 # Four original sustained tones, no borrowed melody. Slow deterministic harmonic opening.
 for i,hz in enumerate([55,82.4069,110,146.8324]):
  phase=2*np.pi*(hz*t+.04*np.sin(t*.11+i))
  amplitude=(.7+.3*np.sin(t*.18+i))*.005
  music[:,0]+=np.sin(phase)*amplitude
  music[:,1]+=np.sin(phase+.06*np.sin(t*.07+i))*amplitude
 air=band_noise(n,84,240,1800)*.0017
 music[:,0]+=air;music[:,1]+=np.roll(air,230)
 swell=.5+.5*np.sin(np.minimum(1,t/(n/RATE))*np.pi)
 music*=swell[:,None]
 music,music_duck=sidechain(v,music,.11)
 fade_in=np.minimum(1,t/1.8);fade_out=np.minimum(1,(n/RATE-t)/1.15)
 music*=(fade_in*fade_out)[:,None]
 sfx*=np.minimum(1,(n/RATE-t)/.15)[:,None]
 mix=v[:,None]+sfx+music
 peak=np.max(np.abs(mix))
 if peak>.89:
  factor=(.89-np.max(np.abs(v)))/max(1e-9,np.max(np.abs(sfx+music)))
  factor=max(.01,min(1,factor));sfx*=factor;music*=factor;mix=v[:,None]+sfx+music
 sf.write(dest/'sfx-stem.wav',sfx/.6,RATE,subtype='PCM_24')
 sf.write(dest/'ambient-stem.wav',music/.12,RATE,subtype='PCM_24')
 closing,_=sf.read(ROOT/'public/audio/brand/closing.wav')
 if closing.ndim==1:closing=np.column_stack([closing,closing])
 final=np.concatenate([mix,closing],axis=0)
 sf.write(dest/'mix.wav',final,RATE,subtype='PCM_24')
 report={'schemaVersion':2,'method':'original-solar-score-v1','seed':42,'sampleRate':RATE,'channels':2,'directionHash':sha(json.dumps(m['direction'],sort_keys=True).encode()),'audioHash':d['bindings']['audioHash'],'stemSha256':sha((dest/'sfx-stem.wav').read_bytes()),'musicStemSha256':sha((dest/'ambient-stem.wav').read_bytes()),'mixSha256':sha((dest/'mix.wav').read_bytes()),'musicFile':'ambient-stem.wav','renderGain':.6,'musicRenderGain':.12,'events':events,'ducking':duck,'musicDucking':music_duck,'predictedMixPeak':float(np.max(np.abs(final))),'externalSamples':False,'humanListeningPerformed':False,'license':'Original project synthesis; no third-party samples. Cinematic effects do not represent sound propagation in space.'}
 write(dest/'sound-design.json',report);export(id)
 print(json.dumps({k:report[k] for k in ['ducking','musicDucking','predictedMixPeak']},indent=2))
if __name__=='__main__':build()
