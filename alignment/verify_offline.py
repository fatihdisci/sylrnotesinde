"""Repeat actual alignment under OS network denial without altering edited production data."""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--id',required=True);a=p.parse_args()
if not __import__('re').fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',a.id):raise ValueError('Invalid ID')
out=ROOT/f'alignment/outputs/{a.id}-offline.json';out.parent.mkdir(exist_ok=True)
probe=subprocess.run(['/usr/bin/sandbox-exec','-p','(version 1) (allow default) (deny network*)',sys.executable,'-c',"import socket\ntry:\n socket.create_connection(('1.1.1.1',443),timeout=1)\n raise SystemExit(1)\nexcept PermissionError: print('network denied')"],check=True,capture_output=True,text=True)
subprocess.run(['/usr/bin/sandbox-exec','-p','(version 1) (allow default) (deny network*)',str(ROOT/'alignment/environments/ctc/bin/python'),str(ROOT/'alignment/align.py'),'--id',a.id,'--output',str(out)],check=True,cwd=ROOT)
old=json.loads((ROOT/f'public/episodes/{a.id}/word-timings.json').read_text());new=json.loads(out.read_text())
assert old['words']==new['words'] and new['metrics']['networkAttempts']==[]
report={'osProbe':probe.stdout.strip(),'identicalWordTimings':True,'networkAttempts':new['metrics']['networkAttempts'],'metrics':new['metrics'],'modelRevision':new['aligner']['revision']}
(ROOT/f'alignment/docs/{a.id}-offline-qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
