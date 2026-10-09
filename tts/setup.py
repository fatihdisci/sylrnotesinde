"""Portable, project-scoped setup. Nothing is installed into the system interpreter."""
import os, platform, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def run(args,**kwargs): subprocess.run([str(x) for x in args],check=True,**kwargs)
def main():
    if platform.system()!='Darwin' or platform.machine()!='arm64':
        raise SystemExit('These locks were verified on Apple Silicon macOS. Other architectures need separate reviewed locks.')
    envroot=ROOT/'environments'; envroot.mkdir(exist_ok=True)
    bootstrap=envroot/'bootstrap'
    if not (bootstrap/'bin/python').exists(): run([sys.executable,'-m','venv',bootstrap])
    uv=bootstrap/'bin/uv'
    if not uv.exists() or subprocess.check_output([uv,'--version'],text=True).strip()!='uv 0.12.24': run([bootstrap/'bin/python','-m','pip','install','uv==0.12.24'])
    env={**os.environ,'UV_PYTHON_INSTALL_DIR':str(envroot/'python'),'UV_CACHE_DIR':str(ROOT/'.cache/uv'),'UV_PYTHON_BIN_DIR':str(envroot/'bin')}
    failed=[]
    unavailable=set()
    for version in ['3.12.12','3.11.15']:
        try: run([uv,'python','install',version],env=env)
        except subprocess.CalledProcessError: unavailable.add(version)
    for model,python in [('antalia-mini','3.12.12'),('ema-lightning','3.12.12'),('supertonic-3','3.11.15')]:
        try:
            if python in unavailable: raise RuntimeError(f'Python {python} unavailable')
            target=envroot/model
            if not (target/'bin/python').exists(): run([uv,'venv','--python',python,target],env=env)
            run([uv,'pip','sync','--python',target/'bin/python',ROOT/'locks'/f'{model}.txt'],env=env)
        except (subprocess.CalledProcessError,RuntimeError): failed.append(model)
    run([sys.executable,ROOT/'download.py'])
    if failed: raise SystemExit(f'Failed environments: {failed}. Other models were retained.')
    if not __import__('shutil').which('ffmpeg'): print('ffmpeg missing. Install ffmpeg before benchmark/normalization.',file=sys.stderr)
    print('Local models ready. Run npm run tts:benchmark; then npm run tts:compare.')
if __name__=='__main__': main()
