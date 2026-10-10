"""Original deterministic stereo film score. Local synthesis; no samples or service."""
import json,math
import numpy as np
import soundfile as sf
from core import ROOT,paths,read,write,sha,export
RATE=48000

def effect(name,frames,seed):
 """Rounded tonal cues: no noise, whoosh, distortion or abrupt sample edges."""
 n=frames*1600;t=np.arange(n)/RATE;duration=n/RATE
 stereo=np.zeros((n,2))
 def bell(hz,at=0,length=.42,level=.10,pan=0):
  local=t-at;active=(local>=0)&(local<length)
  q=np.maximum(0,local)
  envelope=(1-np.exp(-q/.012))*np.exp(-q/(length*.25))
  envelope*=np.clip((length-q)/.04,0,1)*active
  # Nearly pure fundamental with quiet, consonant upper partials.
  tone=(np.sin(2*np.pi*hz*q)+.12*np.sin(2*np.pi*hz*2*q)+.025*np.sin(2*np.pi*hz*3*q))*envelope*level
  stereo[:,0]+=tone*np.sqrt((1-pan)/2)
  stereo[:,1]+=tone*np.sqrt((1+pan)/2)
 if name=='click':bell(659.255,length=.18,level=.11)
 elif name in ['detail','leather']:
  bell(587.33 if name=='detail' else 440,length=.32,level=.09)
 elif name in ['launch','travel','reveal']:
  notes=[293.665,369.994,440,587.33] if name=='reveal' else [293.665,369.994,440]
  spacing=.15 if name=='travel' else .105
  for i,hz in enumerate(notes):bell(hz,i*spacing,.42,.075,-.25+i*.16)
 elif name=='orbit':
  bell(440,length=.38,level=.075,pan=-.18);bell(587.33,.22,.42,.065,.18)
 elif name in ['impact','arrival']:
  bell(293.665,length=.5,level=.11);bell(440,.07,.42,.055)
 elif name in ['bloom','final']:
  for i,hz in enumerate([293.665,369.994,440,587.33]):bell(hz,i*.09,.85,.055 if name=='bloom' else .075)
 else:raise ValueError(f'Unknown tonal cue: {name}')
 # The authored interval remains exact; the cue settles naturally before its end.
 stereo*=np.minimum(1,np.maximum(0,duration-t)/.025)[:,None]
 return stereo

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
 levels=read(ROOT/f'src/episodes/{id}/audio-mix.json')
 if any(not 0<float(levels[k])<=1 for k in ['narration','effects','music']):raise ValueError('Invalid mix levels')
 n=m['timeline']['outroFromFrame']*1600;v=np.pad(voice*.9,(0,n-len(voice)))
 sfx=np.zeros((n,2));events=[]
 for event in m['direction']['events']:
  for i,e in enumerate(event['effects']):
   wave=effect(e['sound'],e['durationFrames'],42+e['frame'])*e['gain'];start=e['frame']*1600
   if start+len(wave)>n:raise ValueError('Effect crosses outro')
   sfx[start:start+len(wave)]+=wave;events.append({**e,'event':event['id'],'id':f'{event["id"]}-{i}'})
 sfx,duck=sidechain(v,sfx,.25)
 t=np.arange(n)/RATE;music=np.zeros((n,2))
 # Quiet consonant sine pad. No noise bed or broadband texture.
 for i,hz in enumerate([146.8324,220,293.6648,369.9944]):
  phase=2*np.pi*hz*t
  amplitude=(.8+.2*np.sin(t*.13+i))*.0025
  music[:,0]+=np.sin(phase)*amplitude
  music[:,1]+=np.sin(phase+.025)*amplitude
 swell=.5+.5*np.sin(np.minimum(1,t/(n/RATE))*np.pi)
 music*=swell[:,None]
 music,music_duck=sidechain(v,music,.11)
 fade_in=np.minimum(1,t/1.8);fade_out=np.minimum(1,(n/RATE-t)/1.15)
 music*=(fade_in*fade_out)[:,None]
 sfx*=np.minimum(1,(n/RATE-t)/.15)[:,None]
 # Preserve the existing tonal shapes and ducking; apply the reviewed balance.
 sfx*=levels['effects']/.6;music*=levels['music']/.12;v*=levels['narration']/.9
 mix=v[:,None]+sfx+music
 peak=np.max(np.abs(mix))
 if peak>.89:
  factor=(.89-np.max(np.abs(v)))/max(1e-9,np.max(np.abs(sfx+music)))
  factor=max(.01,min(1,factor));sfx*=factor;music*=factor;mix=v[:,None]+sfx+music
 sf.write(dest/'sfx-stem.wav',sfx/levels['effects'],RATE,subtype='PCM_24')
 sf.write(dest/'ambient-stem.wav',music/levels['music'],RATE,subtype='PCM_24')
 closing,_=sf.read(ROOT/'public/audio/brand/closing.wav')
 if closing.ndim==1:closing=np.column_stack([closing,closing])
 final=np.concatenate([mix,closing],axis=0)
 sf.write(dest/'mix.wav',final,RATE,subtype='PCM_24')
 report={'schemaVersion':2,'method':'original-solar-tonal-score-v3-balanced','timbre':'rounded sine bells and quiet consonant pad; zero noise generators','seed':42,'sampleRate':RATE,'channels':2,'directionHash':sha(json.dumps(m['direction'],sort_keys=True).encode()),'audioHash':d['bindings']['audioHash'],'stemSha256':sha((dest/'sfx-stem.wav').read_bytes()),'musicStemSha256':sha((dest/'ambient-stem.wav').read_bytes()),'mixSha256':sha((dest/'mix.wav').read_bytes()),'musicFile':'ambient-stem.wav','narrationRenderGain':levels['narration'],'renderGain':levels['effects'],'musicRenderGain':levels['music'],'mixLevels':levels,'events':events,'ducking':duck,'musicDucking':music_duck,'predictedMixPeak':float(np.max(np.abs(final))),'externalSamples':False,'humanListeningPerformed':False,'license':'Original project synthesis; no third-party samples. Cinematic effects do not represent sound propagation in space.'}
 write(dest/'sound-design.json',report);export(id)
 print(json.dumps({k:report[k] for k in ['ducking','musicDucking','predictedMixPeak']},indent=2))
if __name__=='__main__':build()
