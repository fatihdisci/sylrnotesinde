"""Reproducible corpus, all voices, raw + loudness-matched outputs. CPU runs serially."""
import hashlib, json, subprocess, sys, time
from pathlib import Path
from cli import ROOT, MODELS, run_jobs
TESTS=json.loads((ROOT/'test-texts/tests.json').read_text())

def normalize(path):
    dest=path.with_name(path.stem+'-listen.wav')
    analysis=subprocess.run(['ffmpeg','-hide_banner','-nostdin','-i',str(path),'-af','loudnorm=I=-20:TP=-2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    loud=json.loads(analysis.stderr[analysis.stderr.rfind('{'):analysis.stderr.rfind('}')+1])
    af='loudnorm=I=-20:TP=-2:LRA=11:linear=true:print_format=json:'+':'.join(f'{a}={loud[b]}' for a,b in [('measured_I','input_i'),('measured_TP','input_tp'),('measured_LRA','input_lra'),('measured_thresh','input_thresh'),('offset','target_offset')])
    result=subprocess.run(['ffmpeg','-y','-hide_banner','-nostdin','-i',str(path),'-af',af,'-ar','48000','-ac','1','-c:a','pcm_s24le',str(dest)],capture_output=True,text=True,check=True)
    measured=json.loads(result.stderr[result.stderr.rfind('{'):result.stderr.rfind('}')+1])
    meta=json.loads(path.with_suffix('.json').read_text())
    meta.update(listeningPath=str(dest.relative_to(ROOT)),rawPath=str(path.relative_to(ROOT)),loudness=measured,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    # Absolute output paths are machine-local; the tracked catalog is portable.
    meta.pop('output',None)
    return meta

def job(key,voice,test,variant='original',speed=1.):
    text=test['normalized'] if variant=='normalized' else test['text']
    return dict(model=key,voice=voice,test=test['id'],variant=variant,text=text,speed=speed,seed=42,output=str(ROOT/'outputs'/key/voice/f'{test["id"]}-{variant}.wav'))

def main():
    errors=[]
    for key, model in MODELS.items():
        jobs=[]
        for voice in model['voices']:
            for t in TESTS:
                jobs.append(job(key,voice,t))
                if 'normalized' in t: jobs.append(job(key,voice,t,'normalized'))
        pending=[j for j in jobs if not Path(j['output']).with_suffix('.json').exists()]
        try:
            if pending: run_jobs(pending,os_offline=sys.platform=='darwin')
            # Secondary D test: native synthesis speed, target 42 s. Original remains untouched.
            matched=[]
            for voice in model['voices']:
                d=job(key,voice,TESTS[3]); meta=json.loads(Path(d['output']).with_suffix('.json').read_text())
                matched.append(job(key,voice,TESTS[3],'duration-42',meta['durationSeconds']/42.))
            pending=[j for j in matched if not Path(j['output']).with_suffix('.json').exists()]
            if pending: run_jobs(pending,os_offline=sys.platform=='darwin')
        except Exception as e:
            errors.append(dict(model=key,error=str(e)))
            print(f'{key}: {e}',file=sys.stderr,flush=True)
    catalog=[]
    for path in sorted((ROOT/'outputs').glob('*/*/*.wav')):
        if not path.stem.endswith('-listen') and path.with_suffix('.json').exists():
            catalog.append(normalize(path))
    (ROOT/'config/catalog.json').write_text(json.dumps(dict(created=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),records=catalog,errors=errors),ensure_ascii=False,indent=2)+'\n')
    print(f'{len(catalog)} genuine WAV masters and matched listening copies; errors={len(errors)}')
    if errors: sys.exit(1)

if __name__=='__main__': main()
