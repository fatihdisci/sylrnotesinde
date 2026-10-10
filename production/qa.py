"""Measure delivered MP4, not just source WAV. Review status remains separate."""
import argparse,json,math,re,subprocess,sys
from pathlib import Path
import numpy as np,soundfile as sf
from rhythm import inspect_rhythm
from core import ROOT,paths,read,write,sha,verify_current

def pcm(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-ar','48000','-ac','1','-f','f32le','-']),dtype='<f4')
def correlate(source,target,expected):
    margin=4800
    lo=max(0,expected-margin);hi=min(len(target),expected+len(source)+margin)
    window=target[lo:hi];size=1<<(len(window)+len(source)-2).bit_length()
    convolution=np.fft.irfft(np.fft.rfft(window,size)*np.fft.rfft(source[::-1],size),size)
    candidates=convolution[len(source)-1:len(window)]
    offset=int(candidates.argmax());segment=window[offset:offset+len(source)]
    if len(segment)!=len(source):raise ValueError('Truncated encoded audio')
    return (lo+offset-expected)/48,float(np.corrcoef(source,segment)[0,1])
def main():
    p=argparse.ArgumentParser();p.add_argument('--id',required=True);p.add_argument('--video',required=True);p.add_argument('--release',action='store_true');a=p.parse_args()
    data,manifest=verify_current(a.id,a.release);_,dest=paths(a.id);video=Path(a.video)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)]))
    stream=next(s for s in probe['streams'] if s['codec_type']=='video')
    assert (stream['width'],stream['height'],stream['r_frame_rate'],int(stream['nb_read_frames']))==(1080,1920,'30/1',manifest['durationInFrames'])
    source=pcm(dest/'narration.wav');encoded=pcm(video);assert np.isfinite(encoded).all() and np.max(np.abs(encoded))<.99
    offset=manifest['narration'][0]['from']*1600
    # Remove the known, synchronised score for the voice-only diagnostic, while
    # independently correlating the full rendered mix below. Keep the same thresholds.
    accompaniment=np.zeros(len(encoded));narration_gain=.9
    if manifest.get('direction'):
        score=read(dest/'sound-design.json');narration_gain=score.get('narrationRenderGain',.9)
        for file,gain in [('sfx-stem.wav',score['renderGain'])]+([(score['musicFile'],score['musicRenderGain'])] if score.get('musicStemSha256') else []):
            stem=pcm(dest/file)*gain
            accompaniment[:len(stem)]+=stem
    isolated=encoded-accompaniment
    samples=[]
    for label,index in [('start',0),('middle',len(data['words'])//2),('end',len(data['words'])-3)]:
        start=max(0,round(data['words'][index]['startMs']*48)-3840);stop=min(len(source),start+48000)
        lag,corr=correlate(source[start:stop]*narration_gain,isolated,offset+start)
        assert abs(lag)<=1000/30 and corr>.95,(label,lag,corr)
        samples.append({'position':label,'sourceFromMs':start/48,'lagMs':lag,'correlation':corr})
    drift=max(s['lagMs'] for s in samples)-min(s['lagMs'] for s in samples);assert drift<=1000/30
    outro=manifest['durationInFrames']-45;closing=pcm(ROOT/'public/audio/brand/closing.wav');lag,corr=correlate(closing,encoded,outro*1600)
    assert abs(lag)<=1000/30 and corr>.95,('outro',lag,corr)
    assert offset+len(source)<=outro*1600
    # Catch dropped speech / subtitles ending before a measured word, beyond one quantized frame.
    coverage=[]
    for cue in manifest['captions']:
        ws=[data['words'][i] for i in cue['wordIds']];start=(cue['from']-manifest['narration'][0]['from'])*1000/30;end=(cue['to']-manifest['narration'][0]['from'])*1000/30
        assert abs(start-ws[0]['startMs'])<=1000/30+.01 and 0<=end-ws[-1]['endMs']<=1000/30+.01
        coverage.extend(cue['wordIds'])
    assert coverage==list(range(len(data['words'])))
    analysis=subprocess.run(['ffmpeg','-hide_banner','-nostdin','-i',str(video),'-af','loudnorm=I=-20:TP=-2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    loud=json.loads(analysis.stderr[analysis.stderr.rfind('{'):analysis.stderr.rfind('}')+1]);assert float(loud['input_tp'])<=-1.0 and -25<=float(loud['input_i'])<=-17
    black=subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-vf','blackdetect=d=0.03:pix_th=0.02:pic_th=0.98','-an','-f','null','-'],capture_output=True,text=True,check=True)
    black_intervals=re.findall(r'black_start:([\d.]+) black_end:([\d.]+)',black.stderr);assert not black_intervals,black_intervals
    frames_rgb=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-vf','scale=108:192','-f','rawvideo','-pix_fmt','rgb24','-']),dtype=np.uint8).reshape(-1,192,108,3)
    content=frames_rgb[:outro,23:162,7:94].astype(np.int16)
    visible=np.any(np.abs(content-np.array([17,22,21]))>32,axis=-1).sum(axis=(1,2))
    empty_frames=np.where(visible<20)[0].tolist();assert not empty_frames,('empty content frames',empty_frames)
    diffs=np.abs(np.diff(content.astype(np.float32),axis=0)).mean(axis=(1,2,3))/255
    flicker_candidates=(np.where(diffs>.12)[0]+1).tolist()
    # Titles, measurement labels and subtitles must not conceal an empty main image.
    geometry=frames_rgb[:outro,55:123,7:94].astype(np.int16)
    geometry_visible=np.any(np.abs(geometry-np.array([17,22,21]))>32,axis=-1).sum(axis=(1,2))
    empty_geometry_frames=np.where(geometry_visible<20)[0].tolist()
    # Exported SRT and burn-in share the same integer-frame cues, never a second timing source.
    def stamp(f):
        ms=round(f*1000/30);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
    expected='\n\n'.join(f"{i+1}\n{stamp(c['from'])} --> {stamp(c['to'])}\n"+'\n'.join(c['lines']) for i,c in enumerate(manifest['captions']))+'\n'
    assert (dest/'captions.srt').read_text()==expected
    try:
        verify_current(a.id,release=True)
        publication_ready=True;publication_blockers=[]
    except ValueError as error:
        publication_ready=False;publication_blockers=[str(error)]
    result={'id':a.id,'technicalChecksPassed':True,'publicationReady':publication_ready,'publicationBlockers':publication_blockers,'reviewStatus':data['review']['status'],'frames':manifest['durationInFrames'],'fps':30,'seconds':manifest['durationInFrames']/30,'audioDurationSeconds':len(source)/48000,'resultHoldFrames':manifest['timeline']['resultHoldFrames'],'outroFromFrame':outro,'encodedSyncSamples':samples,'driftMs':drift,'encodedPeak':float(np.max(np.abs(encoded))),'integratedLufs':float(loud['input_i']),'truePeakDbtp':float(loud['input_tp']),'outroCorrelation':corr,'outroLagMs':lag,'captionCoverageWords':len(coverage),'srtMatchesBurnIn':True,'blackIntervals':black_intervals,'emptyContentFrames':empty_frames,'largeFrameChangeCandidates':flicker_candidates,'suspiciousWords':[w['id'] for w in data['words'] if w['issues']],'humanListeningPerformed':False,'humanReviewListeningRecorded':bool(data['review'].get('listened')),'manualChecksRequired':['Listen to Turkish pronunciation, numbers, units and last syllables.','Inspect word onsets/offsets in the local editor; CTC20ms resolution does not guarantee33ms accuracy.','Watch the actual MP4 for semantic scene timing, flicker and subjective readability.'],'audioSha256':sha((dest/'narration.wav').read_bytes()),'wordTimingsSha256':sha((dest/'word-timings.json').read_bytes())}
    result['emptyGeometryFramesForReview']=empty_geometry_frames
    result['rhythm']=inspect_rhythm(frames_rgb[:outro],encoded[:outro*1600],annotations=data['script'].get('intentionalPauses',[]))
    if manifest.get('direction'):
        score=read(dest/'sound-design.json');stem=pcm(dest/'sfx-stem.wav')*score['renderGain']
        mix=np.zeros(outro*1600);mix[offset:offset+len(source)]+=source*narration_gain;mix[:len(stem)]+=stem
        if score.get('musicStemSha256'):
            music=pcm(dest/score['musicFile'])*score['musicRenderGain'];mix[:len(music)]+=music
        mix_samples=[]
        for event in manifest['direction']['events']:
            start=event['from']*1600;stop=min(len(mix),start+24000)
            if stop-start<4800:continue
            event_lag,event_corr=correlate(mix[start:stop],encoded,start)
            assert abs(event_lag)<=1000/30 and event_corr>.98,('effect/voice mix',event['id'],event_lag,event_corr)
            mix_samples.append({'event':event['id'],'frame':event['from'],'lagMs':event_lag,'correlation':event_corr})
        result['soundDesign']={'events':len(score['events']),'ducking':score['ducking'],'renderedMixChecks':mix_samples,'separateStemSha256':score['stemSha256'],'humanAudibilityReviewPerformed':False}
        result['storyboard']={'hash':manifest['direction']['storyboardHash'],'events':len(manifest['direction']['events']),'timingSource':'measured words with explicit authored anchors','speechOnsetMs':manifest['direction']['speech']['onsetMs'],'speechOffsetMs':manifest['direction']['speech']['offsetMs']}
    write(video.parent/'qa.json',result)
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
