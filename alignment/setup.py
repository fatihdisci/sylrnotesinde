"""Install a separate pinned CPU aligner and download assets once, inside this project."""
import hashlib,json,os,subprocess,sys,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent
SPEC={'repo':'mpoyraz/wav2vec2-xls-r-300m-cv7-turkish','revision':'708639f50559d7970f462e13ec64d3f059ca89f6','license':'CC-BY-4.0','engine':'ctc-viterbi-v1','sampleRate':16000,'frameStrideMs':20}
FILES=['config.json','preprocessor_config.json','special_tokens_map.json','tokenizer_config.json','vocab.json','pytorch_model.bin','README.md']
def main():
    uv=PROJECT/'tts/environments/bootstrap/bin/uv'
    if not uv.exists():raise SystemExit('Run npm run tts:setup first (selected Supertonic only).')
    python=PROJECT/'tts/environments/python/cpython-3.11.15-macos-aarch64-none/bin/python3.11'
    env={**os.environ,'UV_CACHE_DIR':str(ROOT/'.cache/uv')}
    target=ROOT/'environments/ctc'
    if not (target/'bin/python').exists():subprocess.run([str(uv),'venv','--python',str(python),str(target)],env=env,check=True)
    subprocess.run([str(uv),'pip','sync','--python',str(target/'bin/python'),str(ROOT/'locks/macos-arm64.txt')],env=env,check=True)
    spec=json.loads((ROOT/'model.json').read_text())
    dest=ROOT/'models/turkish';dest.mkdir(parents=True,exist_ok=True)
    for entry in spec['files']:
        p=dest/entry['path']
        def valid():return p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256']
        if not valid():
            url=f"https://huggingface.co/{spec['repo']}/resolve/{spec['revision']}/{entry['path']}"
            with urllib.request.urlopen(url,timeout=120) as response,open(p.with_suffix(p.suffix+'.part'),'wb') as out:
                import shutil;shutil.copyfileobj(response,out)
            p.with_suffix(p.suffix+'.part').replace(p)
        if not valid():raise ValueError(f'Checksum mismatch: {p}')
        print('Verified '+entry['path'],flush=True)
if __name__=='__main__':main()
