"""Fetch pinned public assets; no runtime networking. Existing files are verified."""
from pathlib import Path
import argparse, concurrent.futures, hashlib, json, urllib.request, shutil
from selection import add_selection_arguments, selected_models
ROOT = Path(__file__).resolve().parent
CHECKSUM_FILE=ROOT/'config/asset-checksums.json'
EXPECTED=json.loads(CHECKSUM_FILE.read_text()) if CHECKSUM_FILE.exists() else {}

def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()

def fetch(item):
    key, model, info = item
    path = ROOT/'models'/key/info['path']
    path.parent.mkdir(parents=True, exist_ok=True)
    expected=info['sha256'] or EXPECTED.get(str(path.relative_to(ROOT)))
    def valid():
        return path.exists() and path.stat().st_size == info['size'] and (not expected or digest(path) == expected)
    if not valid():
        url = f"https://huggingface.co/{model['repo']}/resolve/{model['revision']}/{info['path']}"
        temp = path.with_suffix(path.suffix+'.part')
        with urllib.request.urlopen(url, timeout=120) as response, open(temp, 'wb') as out:
            shutil.copyfileobj(response, out, length=1024*1024)
        temp.replace(path)
    if not valid(): raise ValueError(f'Invalid asset: {path}')
    return str(path.relative_to(ROOT)), digest(path)

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__); add_selection_arguments(parser)
    args=parser.parse_args(); models=selected_models(args.model,args.all)
    records=[];errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures=[pool.submit(fetch,(k,m,f)) for k,m in models.items() for f in m['files']]
        for future in concurrent.futures.as_completed(futures):
            try: records.append(future.result())
            except Exception as error: errors.append(str(error))
    if not CHECKSUM_FILE.exists() and not errors: CHECKSUM_FILE.write_text(json.dumps(dict(sorted(records)),indent=2)+'\n')
    for key in models:
        for name in ['LICENSE','NOTICE','README.md']:
            source = ROOT/'models'/key/name
            if source.exists():
                dest = ROOT/'docs/licenses'/key/name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source,dest)
    print(f'Verified {len(records)} local assets.')
    if errors: raise SystemExit('Some assets failed; other downloads were retained: '+str(errors))
