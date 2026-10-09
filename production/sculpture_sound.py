"""Original layered Foley for the isolated time-sculpture candidate. No external samples."""
import numpy as np
import sound
from core import paths,read
base=sound.synth

def sculptural(name,frames,rate=48000):
    n=frames*1600;t=np.arange(n)/rate;p=np.arange(n)/max(1,n-1)
    rng=np.random.default_rng(20261009+sum(map(ord,name)))
    noise=rng.normal(0,1,n)
    low=np.convolve(noise,np.hanning(81)/np.hanning(81).sum(),mode='same')
    mid=noise-np.convolve(noise,np.ones(11)/11,mode='same')
    def sweep(a,b):return np.sin(2*np.pi*(a*t+(b-a)*t*t/(2*n/rate)))
    fade=np.minimum(1,t/.004)*np.minimum(1,(n/rate-t)/.08)
    if name in ['scale','riser','coil']:
        # Air movement + two detuned resonances + sub arrival, no sustained music bed.
        wind=low*3.8*np.sin(np.pi*p)**1.8+mid*.09*np.sin(np.pi*p)**2
        tone=(sweep(95,34)*.48+sweep(191,69)*.19)*np.sin(np.pi*p)**1.2
        if name=='riser':tone=(sweep(38,130)*.42+sweep(76,260)*.12)*np.sin(np.pi*p)**1.2
        x=wind+tone
    elif name in ['fold','paper','swish']:
        x=(low*4+mid*.11)*np.sin(np.pi*p)**1.6
        for pos in [.16,.38,.64,.82]:
            dt=t-pos*n/rate
            x+=(np.sin(2*np.pi*370*t)*.12+mid*.13)*np.exp(-np.maximum(0,dt)*100)*(dt>=0)
        if name=='fold':x+=sweep(170,52)*np.exp(-p*5)*.45
    elif name in ['latch','impact','resolve']:
        x=np.zeros(n)
        for hz,level,decay in [(74,.55,6),(151,.26,13),(410,.17,21),(1370,.11,42),(2820,.06,65)]:
            x+=np.sin(2*np.pi*hz*t)*level*np.exp(-t*decay)
        x+=mid*.16*np.exp(-t*45)
        if name=='impact':x+=sweep(92,33)*.4*np.exp(-t*5)
        if name=='resolve':x*=.7
    else:x=base(name,frames,rate)
    x*=fade
    return x/max(.01,float(np.max(np.abs(x))))*.85

if __name__=='__main__':
    # The existing mixer keeps exact event frames, waveform sidechain and hash binding.
    sound.synth=sculptural
    sound.build('seconds-sculpture',speech_ratio=.48,master_gain=.42)
    _,dest=paths('seconds-sculpture')
    # Method identity must remain explicit and be hashed back into the manifest.
    score=read(dest/'sound-design.json');score['method']='time-sculpture-original-layered-foley-v1';score['seed']=20261009
    sound.write(dest/'sound-design.json',score);sound.export('seconds-sculpture')
