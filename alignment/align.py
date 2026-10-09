"""Known Turkish text -> real waveform, CTC Viterbi. No transcription or interpolation."""
import argparse,json,os,sys,time,resource,subprocess,unicodedata,difflib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HOME=str(ROOT/'alignment/.cache/hf'),OMP_NUM_THREADS='2')
network=[]
def offline(event,args):
    if event in ('socket.connect','socket.getaddrinfo','socket.sendto'):network.append(event);raise PermissionError('Offline alignment')
sys.addaudithook(offline)
sys.path.insert(0,str(ROOT/'production'))
from core import paths,read,write,spoken,bindings,sha,word_errors

def viterbi(logp,tokens,blank):
    import numpy as np
    states=np.full(len(tokens)*2+1,blank,dtype=np.int64);states[1::2]=tokens
    n=len(states);prev=np.full(n,-np.inf);prev[0]=logp[0,blank];prev[1]=logp[0,tokens[0]]
    back=np.zeros((len(logp),n),dtype=np.int8)
    allowed=np.zeros(n,dtype=bool);allowed[2:]=(states[2:]!=blank)&(states[2:]!=states[:-2])
    for t in range(1,len(logp)):
        one=np.r_[-np.inf,prev[:-1]];two=np.r_[-np.inf,-np.inf,prev[:-2]];two[~allowed]=-np.inf
        choices=np.stack([prev,one,two]);best=choices.argmax(axis=0);back[t]=best
        prev=choices[best,np.arange(n)]+logp[t,states]
    state=n-1 if prev[-1]>prev[-2] else n-2
    if not np.isfinite(prev[state]):raise ValueError('No complete CTC path; do not invent timings')
    path=[]
    for t in range(len(logp)-1,-1,-1):path.append(state);state-=int(back[t,state])
    path.reverse();return np.array(path),states

def main():
    p=argparse.ArgumentParser();p.add_argument('--id',required=True);p.add_argument('--output');args=p.parse_args()
    import numpy as np,torch
    from transformers import Wav2Vec2ForCTC,Wav2Vec2FeatureExtractor
    torch.set_num_threads(2);torch.manual_seed(42)
    specpath,dest=paths(args.id);spec=read(specpath);audio=dest/'narration.wav'
    start=time.perf_counter();modelpath=ROOT/'alignment/models/turkish';vocab=read(modelpath/'vocab.json');modelSpec=read(ROOT/'alignment/model.json')
    words=spoken(spec).split();chars=[];owners=[];normalizations=[]
    for i,word in enumerate(words):
        clean=unicodedata.normalize('NFC',word).replace('İ','i').replace('I','ı').lower()
        clean=''.join(c for c in clean if c.isalpha()).replace('â','a').replace('î','i').replace('û','u')
        if any(c.isdigit() for c in word):raise ValueError('Spell numbers in spoken text; keep numeric display mapping separately')
        if not clean or any(c not in vocab for c in clean):raise ValueError(f'Unsupported spoken word: {word}')
        if i:chars.append('|');owners.append(-1)
        chars.extend(clean);owners.extend([i]*len(clean));normalizations.append(clean)
    tokens=[vocab[c] for c in chars]
    pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(audio),'-ac','1','-ar','16000','-f','f32le','-'])
    wav=np.frombuffer(pcm,dtype='<f4').copy();seconds=len(wav)/16000
    if seconds>90:raise ValueError('This short-video CPU aligner accepts <=90s per file')
    extractor=Wav2Vec2FeatureExtractor.from_pretrained(str(modelpath),local_files_only=True)
    model=Wav2Vec2ForCTC.from_pretrained(str(modelpath),local_files_only=True).eval()
    with torch.inference_mode():
        inputs=extractor(wav,sampling_rate=16000,return_tensors='pt')
        logits=model(**inputs).logits[0];logp=torch.log_softmax(logits,dim=-1).cpu().numpy()
    path,states=viterbi(logp,tokens,model.config.pad_token_id)
    stride=np.prod(model.config.conv_stride)/16000*1000
    results=[]
    for i,word in enumerate(words):
        positions=[j for j,owner in enumerate(owners) if owner==i];frames=np.where(np.isin(path,[2*j+1 for j in positions]))[0]
        if not len(frames):raise ValueError(f'Unaligned word {i}: {word}')
        score=float(np.exp(logp[frames,states[path[frames]]]).mean());a=float(frames[0]*stride);b=min(seconds*1000,float((frames[-1]+1)*stride))
        issues=[]
        if score<.55:issues.append('low_ctc_score')
        if b-a<60:issues.append('short_word')
        if b-a>1500:issues.append('long_word')
        results.append({'id':i,'word':word,'alignmentText':normalizations[i],'startMs':round(a,3),'endMs':round(b,3),'confidence':round(score,5),'reviewStatus':'needs_review' if issues else 'automatic','issues':issues,'corrections':[]})
    # Extend sparse CTC letter spikes to nearby acoustic edges; bounded by adjacent
    # words and real10ms RMS windows. This is a measured refinement, not a speed estimate.
    for i,word in enumerate(results):
        original=(word['startMs'],word['endMs'])
        lower=max(results[i-1]['endMs'] if i else 0,word['startMs']-120)
        upper=min(results[i+1]['startMs'] if i+1<len(results) else seconds*1000,word['endMs']+180)
        a=word['startMs'];b=word['endMs']
        while a-10>=lower:
            window=wav[round((a-10)*16):round(a*16)]
            if np.sqrt(np.mean(window**2))<.004:break
            a-=10
        while b+10<=upper:
            window=wav[round(b*16):round((b+10)*16)]
            if np.sqrt(np.mean(window**2))<.004:break
            b+=10
        word['startMs']=a;word['endMs']=b
        if original!=(a,b):word['acousticRefinement']={'ctcStartMs':original[0],'ctcEndMs':original[1],'method':'bounded10ms-rms-edge-v1'}
    gaps=[]
    for a,b in zip(results,results[1:]):
        if b['startMs']-a['endMs']>300:
            samples=wav[round(a['endMs']*16):round(b['startMs']*16)];rms=float(np.sqrt(np.mean(samples**2)))
            if rms>.015:gaps.append({'startMs':a['endMs'],'endMs':b['startMs'],'rms':rms,'reviewed':False})
    # Greedy decoding is only a diagnostic of the same logits, never the timing source.
    ids=logp.argmax(axis=-1);dedup=[int(x) for i,x in enumerate(ids) if (i==0 or x!=ids[i-1]) and x!=model.config.pad_token_id]
    inverse={v:k for k,v in vocab.items()};diagnostic=''.join(inverse[x] for x in dedup).replace('|',' ')
    expected=[w['alignmentText'] for w in results]
    for tag,i,j,_,_ in difflib.SequenceMatcher(None,expected,diagnostic.split(),autojunk=False).get_opcodes():
        if tag!='equal':
            for word in results[i:j]:word['issues'].append('diagnostic_text_mismatch');word['reviewStatus']='needs_review'
    energy=[round(float(np.sqrt(np.mean(wav[i:i+320]**2))),6) for i in range(0,len(wav),320)]
    data={'schemaVersion':1,'id':args.id,'script':spec,'bindings':bindings(specpath,audio),'alignerHash':sha((ROOT/'alignment/model.json').read_bytes()),'aligner':modelSpec,'audioDurationMs':round(seconds*1000,3),'frameResolutionMs':float(stride),'words':results,'displayMap':[],'unexplainedSpeechGaps':gaps,'energy20ms':energy,'review':{'status':'needs_review','reviewer':None,'listened':False},'diagnosticGreedyText':diagnostic,'metrics':{'seconds':time.perf_counter()-start,'peakRssMiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2,'networkAttempts':network}}
    offset=0
    for i,phrase in enumerate(spec['phrases']):
        n=len(phrase['spoken'].split());data['displayMap'].append({'phrase':i,'display':phrase['display'],'spokenWordIds':list(range(offset,offset+n))});offset+=n
    write(Path(args.output) if args.output else dest/'word-timings.json',data)
    errors=word_errors(data)
    if errors:raise ValueError('; '.join(errors))
    print(json.dumps({'words':len(results),'suspectWords':sum(bool(w['issues']) for w in results),'seconds':data['metrics']['seconds'],'diagnostic':diagnostic},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
