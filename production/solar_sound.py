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

def rhythmic_bed(n):
 """Original 88 BPM score: an eight-bar melody, warm keys and a restrained groove.

 Dmaj9 / Bm9 / Gmaj9 / Asus4-A. Three arranged sections replace the
 perpetual eighth-note arpeggio. Deterministic additive synthesis, no samples.
 """
 out=np.zeros((n,2));beat=60/88;bar=4*beat;duration=n/RATE
 def hz(midi):return 440*2**((midi-69)/12)
 def note(at,midi,length,level,pan=0,kind='keys'):
  start=round(at*RATE);count=min(round(length*RATE),n-start)
  if count<=0 or start<0:return
  t=np.arange(count)/RATE;frequency=hz(midi)
  release=np.minimum(1,np.maximum(0,length-t)/.12)
  if kind=='pad':
   env=(1-np.exp(-t/.42))*np.exp(-t/9)*release
   wave=(np.sin(2*np.pi*frequency*t)+.18*np.sin(2*np.pi*frequency*2*t))
  elif kind=='kick':
   env=(1-np.exp(-t/.006))*np.exp(-t/.075)*release
   phase=2*np.pi*(49*t+34*.023*(1-np.exp(-t/.023)))
   wave=np.sin(phase)
  elif kind=='rim':
   env=(1-np.exp(-t/.003))*np.exp(-t/.024)*release
   wave=.65*np.sin(2*np.pi*620*t)+.22*np.sin(2*np.pi*930*t)+.13*np.sin(2*np.pi*1240*t)
  elif kind=='tick':
   env=(1-np.exp(-t/.003))*np.exp(-t/.014)*release
   wave=.7*np.sin(2*np.pi*1760*t)+.3*np.sin(2*np.pi*2640*t)
  elif kind=='bass':
   env=(1-np.exp(-t/.026))*np.exp(-t/.65)*release
   wave=np.sin(2*np.pi*frequency*t)+.12*np.sin(2*np.pi*frequency*2*t)
  else:
   # Felt-key-like fundamental with independently decaying soft overtones.
   env=(1-np.exp(-t/.012))*release
   wave=sum(amp*np.sin(2*np.pi*frequency*partial*t)*np.exp(-t/decay)
            for partial,amp,decay in [(1,1,1.05),(2,.22,.56),(3,.055,.24),(4,.018,.16)])
  wave*=env*level
  out[start:start+count,0]+=wave*np.sqrt((1-pan)/2)
  out[start:start+count,1]+=wave*np.sqrt((1+pan)/2)
 # Two bars per harmony; open voicings leave the narrator's midrange room.
 chords=[([50,57,61,64],38),([47,54,57,61],35),([43,50,54,57],31),([45,52,57,62],33)]
 # A question-and-answer melody with actual rests, longer endings and variation.
 phrases=[[(.5,74,1),(2,78,.75),(3.5,76,1.5),(6,69,1.5)],
          [(0,71,1.5),(2.5,74,1),(4,73,1),(5.5,69,2)],
          [(.5,71,1),(2,74,1.5),(4.5,78,1),(6,76,1.5)],
          [(0,74,1.5),(2,73,.75),(3.5,69,1.5),(6,73,1.5)]]
 bars=math.ceil(duration/bar)
 for index in range(bars):
  at=index*bar;cycle=index//8;within=index%8;chord,root=chords[within//2]
  opening=index<2;ending=at>duration-8
  # Short introduction, fuller middle, spacious final sentence.
  activity=.55 if opening else (.48 if ending else (1 if cycle else .82))
  if index%2==0:
   for j,midi in enumerate(chord):note(at+j*.028,midi,bar*2+.35,.0038,-.48+j*.32,'pad')
  # Sparse offbeat chord stabs alternate with the lead instead of playing every step.
  for beat_at in ([1.5] if opening or ending else [1.5,3.25]):
   for j,midi in enumerate(chord[1:]):note(at+beat_at*beat+j*.018,midi,1.2,.0042*activity,-.3+j*.3)
  if not ending:
   for pulse,level in [(0,.041),(1.75,.019),(2.5,.032)]:
    note(at+pulse*beat,0,.3,level*activity,0,'kick')
   for pulse in [1,3]:note(at+pulse*beat,0,.14,.0075*activity,.16,'rim')
   for pulse in [.5,1.5,2.5,3.5]:note(at+pulse*beat,0,.09,.0016*activity,-.3 if pulse<2 else .3,'tick')
  for pulse,midi in [(0,root),(2.5,root+12)]:note(at+pulse*beat,midi,.95,.018*activity,0,'bass')
  if index%2==0:
   for position,midi,hold in phrases[within//2]:
    # Second statement answers one octave down; final phrase settles on D.
    if cycle==1 and position<2:midi-=12
    if ending:midi=74 if position==6 else midi
    length=min(hold*beat+1,2.6);gain=.014 if opening else .017
    note(at+position*beat,midi,length,gain,-.12 if position<4 else .12)
    # Two quiet, musical echoes; all tails are clipped at the fixed outro boundary.
    note(at+(position+.75)*beat,midi,length,gain*.17,.48)
    note(at+(position+1.5)*beat,midi,length,gain*.07,-.48)
 # Conclude on an open Dmaj9; do not leave the final phrase on the dominant.
 resolve=max(0,duration-4.7)
 for j,midi in enumerate([50,57,61,64,74]):note(resolve+j*.065,midi,4.4,.0045,-.4+j*.2,'pad')
 return out

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
   wave=effect(e['sound'],e['durationFrames'],42+e['frame'])*e['gain']*1.2;start=e['frame']*1600
   if start+len(wave)>n:raise ValueError('Effect crosses outro')
   sfx[start:start+len(wave)]+=wave;events.append({**e,'event':event['id'],'id':f'{event["id"]}-{i}'})
 sfx,duck=sidechain(v,sfx,.32)
 t=np.arange(n)/RATE;music=rhythmic_bed(n)
 swell=.5+.5*np.sin(np.minimum(1,t/(n/RATE))*np.pi)
 music*=swell[:,None]
 music,music_duck=sidechain(v,music,.18)
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
 report={'schemaVersion':2,'method':'original-solar-melodic-score-v5','timbre':'rounded bells;88 BPM warm keys,eight-bar melody,open chords,syncopated bass and soft tonal groove; zero noise generators','rhythm':{'bpm':88,'meter':'4/4','originalComposition':True,'key':'D major','form':'eight-bar theme; introduction,answer,development,spacious resolution','harmony':['Dmaj9','Bm9','Gmaj9','Asus4-A'],'noiseGenerators':0},'seed':42,'sampleRate':RATE,'channels':2,'directionHash':sha(json.dumps(m['direction'],sort_keys=True).encode()),'audioHash':d['bindings']['audioHash'],'stemSha256':sha((dest/'sfx-stem.wav').read_bytes()),'musicStemSha256':sha((dest/'ambient-stem.wav').read_bytes()),'mixSha256':sha((dest/'mix.wav').read_bytes()),'musicFile':'ambient-stem.wav','narrationRenderGain':levels['narration'],'renderGain':levels['effects'],'musicRenderGain':levels['music'],'mixLevels':levels,'events':events,'ducking':duck,'musicDucking':music_duck,'predictedMixPeak':float(np.max(np.abs(final))),'externalSamples':False,'humanListeningPerformed':False,'license':'Original project synthesis; no third-party samples. Cinematic effects do not represent sound propagation in space.'}
 write(dest/'sound-design.json',report);export(id)
 print(json.dumps({k:report[k] for k in ['ducking','musicDucking','predictedMixPeak']},indent=2))
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--id',default='solar-basketball')
 build(parser.parse_args().id)
