"""Install only the optional pinned Chatterbox environment and weights."""
import os,json,subprocess,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def run(args,**kw):subprocess.run([str(a) for a in args],check=True,cwd=ROOT,**kw)
def main():
 config=json.loads((ROOT/'tts/config/chatterbox.json').read_text())
 uv=ROOT/'tts/environments/bootstrap/bin/uv'
 if not uv.exists():raise SystemExit('Prepare the existing project uv bootstrap first; no system installation is performed.')
 vendor=ROOT/'tts/vendor/chatterbox';venv=ROOT/'tts/environments/chatterbox'
 if not vendor.exists():run(['git','clone',config['repository'],vendor])
 if subprocess.check_output(['git','-C',str(vendor),'rev-parse','HEAD'],text=True).strip()!=config['codeRevision']:
  if subprocess.check_output(['git','-C',str(vendor),'status','--porcelain'],text=True).strip():raise ValueError('Chatterbox vendor has local changes; do not overwrite')
  run(['git','-C',vendor,'fetch','origin',config['codeRevision']]);run(['git','-C',vendor,'checkout',config['codeRevision']])
 env={**os.environ,'UV_PYTHON_INSTALL_DIR':str(ROOT/'tts/environments/python'),'UV_CACHE_DIR':str(ROOT/'tts/.cache/uv')}
 run([uv,'python','install',config['python']],env=env)
 if not (venv/'bin/python').exists():run([uv,'venv','--python',config['python'],venv],env=env)
 run([uv,'pip','sync','--python',venv/'bin/python',ROOT/'tts/locks/chatterbox.txt'],env=env)
 code="from huggingface_hub import snapshot_download; snapshot_download(repo_id="+repr(config['modelRepository'])+", revision="+repr(config['modelRevision'])+", local_dir='tts/models/chatterbox', allow_patterns="+repr(config['files'])+")"
 run([venv/'bin/python','-c',code])
 checks={f:hashlib.sha256((ROOT/'tts/models/chatterbox'/f).read_bytes()).hexdigest() for f in config['files']}
 expected=json.loads((ROOT/'tts/config/chatterbox-assets.json').read_text())
 if checks!=expected:raise ValueError('Chatterbox model checksum mismatch')
 print('Optional Chatterbox ready; existing M1 and Antalia environments untouched.')
if __name__=='__main__':main()
