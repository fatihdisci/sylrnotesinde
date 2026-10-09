"""Review-only rhythm diagnostics. Pauses are evidence to inspect, never automatic failure."""
import numpy as np

def intervals(mask,fps,minimum=2):
    edges=np.flatnonzero(np.diff(np.r_[False,mask,False].astype(int)))
    return [{'fromFrame':int(a),'toFrame':int(b),'fromSeconds':round(a/fps,3),'toSeconds':round(b/fps,3),'durationSeconds':round((b-a)/fps,3)} for a,b in zip(edges[::2],edges[1::2]) if b-a>=minimum*fps]

def inspect_rhythm(rgb,pcm,fps=30,sample_rate=48000,annotations=()):
    # Full content viewport excludes the fixed signature and subtitle region.
    visual=rgb[:,55:145,7:94].astype(np.float32)
    delta=np.r_[1,np.abs(np.diff(visual,axis=0)).mean(axis=(1,2,3))/255]
    near_static=delta<.0006
    per_frame=sample_rate//fps
    padded=np.pad(pcm,(0,max(0,len(rgb)*per_frame-len(pcm))))[:len(rgb)*per_frame]
    rms=np.sqrt(np.mean(padded.reshape(len(rgb),per_frame)**2,axis=1))
    quiet=rms<10**(-48/20)
    combined=intervals(quiet&near_static,fps)
    for span in combined:
        span['reviewRequired']=True
        span['authorNotes']=[a['purpose'] for a in annotations if a['from']<span['toFrame'] and a['to']>span['fromFrame']]
    return {'mode':'review-only','audioSilenceThresholdDbfs':-48,'meanPixelDeltaThreshold':.0006,'minimumSeconds':2,'silentIntervals':intervals(quiet,fps),'nearlyStaticIntervals':intervals(near_static,fps),'silentAndNearlyStaticIntervals':combined,'automaticFailure':False}
