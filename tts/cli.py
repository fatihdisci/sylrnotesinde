"""Stable, stdlib-only dispatcher; inference never runs in the system interpreter."""
import argparse, json, os, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
MODELS=json.loads((ROOT/'config/models.json').read_text())

def run_jobs(jobs, device='cpu', os_offline=False):
    model=jobs[0]['model']
    if any(j['model']!=model for j in jobs): raise ValueError('One model per inference process')
    for j in jobs:
        if j['voice'] not in MODELS[model]['voices']: raise ValueError('Unknown voice')
        if not .5 <= j.get('speed',1.) <= 2.: raise ValueError('Speed multiplier must be 0.5–2')
    executable=ROOT/'environments'/model/'bin/python'
    if not executable.exists(): raise RuntimeError('Run npm run tts:setup first')
    with tempfile.NamedTemporaryFile(mode='w',suffix='.json',encoding='utf-8',dir=ROOT/'outputs') as f:
        json.dump(jobs,f,ensure_ascii=False); f.flush()
        cmd=[str(executable),str(ROOT/'worker.py'),'--jobs',f.name,'--device',device]
        if os_offline:
            cmd=['/usr/bin/sandbox-exec','-p','(version 1) (allow default) (deny network*)',*cmd]
        subprocess.run(cmd,check=True,cwd=ROOT.parent)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model',choices=list(MODELS))
    p.add_argument('--voice')
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument('--text'); group.add_argument('--text-file')
    p.add_argument('--speed',type=float,help='Relative to model native default, no audio time stretch')
    p.add_argument('--seed',type=int)
    p.add_argument('--output',required=True)
    p.add_argument('--device',choices=['cpu','mps'])
    p.add_argument('--os-offline',action='store_true')
    a=p.parse_args()
    config=json.loads((ROOT/'config/narrator.json').read_text())
    model=a.model or config['activeModel']
    if not model: p.error('No narrator selected. Supply --model for a comparison candidate.')
    voice=a.voice or config['settings'][model]['voice']
    text=Path(a.text_file).read_text().strip() if a.text_file else a.text
    if not text.strip(): p.error('Empty text')
    ROOT.joinpath('outputs').mkdir(exist_ok=True)
    run_jobs([dict(model=model,voice=voice,text=text,speed=a.speed if a.speed is not None else config['settings'][model]['speed'],seed=a.seed if a.seed is not None else config['seed'],output=str(Path(a.output).resolve()))],a.device or config['device'],a.os_offline)

if __name__=='__main__': main()
