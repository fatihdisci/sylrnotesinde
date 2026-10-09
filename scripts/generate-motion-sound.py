"""Original, seeded synthesis. No samples, models, network or third-party sound license."""
import math,random,struct,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RATE=48000
SPECS={'tick':(.20,900,1800,.26),'unfold':(.60,170,680,.18),'merge':(.60,480,160,.22),'depth':(1.20,180,55,.23),'settle':(.50,260,100,.22),'reveal':(.80,200,400,.20)}
def synth(name,seconds,a,b,gain):
    rng=random.Random(42);samples=[];phase=0;low=0
    for i in range(round(seconds*RATE)):
        t=i/RATE;p=t/seconds
        frequency=a*(b/a)**p;phase+=2*math.pi*frequency/RATE
        envelope=min(1,t/.012)*min(1,(seconds-t)/.12)*math.exp(-p*(8 if name=='tick' else 2))
        noise=rng.uniform(-1,1);low=.96*low+.04*noise
        value=math.sin(phase)*.65+math.sin(phase*1.51)*.15+low*.6
        if name=='unfold':value=low*2+math.sin(phase)*.15
        samples.append(round(max(-1,min(1,value*envelope*gain))*32767))
    path=ROOT/f'public/audio/motion/{name}.wav';path.parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(path),'wb') as out:
        out.setparams((1,2,RATE,0,'NONE','not compressed'));out.writeframes(struct.pack('<'+'h'*len(samples),*samples))
if __name__=='__main__':
    for name,spec in SPECS.items():synth(name,*spec)
    print('6 original procedural motion sounds generated at48kHz; seed42.')
