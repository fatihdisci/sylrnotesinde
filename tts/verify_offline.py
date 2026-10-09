"""Independent repeat with macOS network sandbox, integrity check and fixed seed comparison."""
import hashlib, json, subprocess, sys
from pathlib import Path
from cli import ROOT, MODELS, run_jobs

def main():
    if sys.platform!='darwin': raise SystemExit('OS network-isolation verification is macOS-specific.')
    probe=subprocess.run(['/usr/bin/sandbox-exec','-p','(version 1) (allow default) (deny network*)',sys.executable,'-c',"import socket\ntry:\n socket.create_connection(('1.1.1.1',443),timeout=2)\n raise SystemExit(1)\nexcept PermissionError:\n print('OS network denied')"],capture_output=True,text=True,check=True)
    text=json.loads((ROOT/'test-texts/tests.json').read_text())[0]['text']
    records=[]
    for model,spec in MODELS.items():
        voice=spec['voices'][0]
        path=ROOT/'outputs/diagnostics/offline'/model/'A.wav'
        run_jobs([dict(model=model,voice=voice,text=text,speed=1.,seed=42,output=str(path))],os_offline=True)
        first=ROOT/'outputs'/model/voice/'A-original.wav'
        metadata=json.loads(path.with_suffix('.json').read_text());metadata['output']=str(path.relative_to(ROOT))
        def pcm_hash(file):
            return subprocess.check_output(['ffmpeg','-v','error','-i',str(file),'-map','0:a','-c:a','pcm_f32le','-f','hash','-hash','sha256','-'],text=True).strip()
        metadata['identicalDecodedSamples']=pcm_hash(path)==pcm_hash(first)
        metadata['decodedPcmSha256']=pcm_hash(path).split('=')[1]
        records.append(metadata)
    result=dict(osNetworkProbe=probe.stdout.strip(),method='sandbox-exec deny network* + Python network audit hook; Mac network interfaces left enabled',records=records)
    (ROOT/'config/offline-test.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    if any(r['networkAttempts'] or not r['identicalDecodedSamples'] for r in records): raise SystemExit('Offline determinism/network check failed; inspect report')
    print('Three independent offline repeats succeeded; all decoded samples are identical at seed 42 (WAV PEAK timestamps may differ).')
if __name__=='__main__': main()
