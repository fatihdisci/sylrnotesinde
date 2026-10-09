"""Real waveform checks. Run with a model venv; stdlib dispatcher otherwise."""
import json, subprocess, sys
from pathlib import Path
from selection import narrator_config
ROOT=Path(__file__).resolve().parent
if sys.prefix==sys.base_prefix:
    raise SystemExit(subprocess.call([str(ROOT/'environments'/ (narrator_config()['activeModel'] or 'supertonic-3') /'bin/python'),__file__]))
import numpy as np, soundfile as sf

def main():
    catalog=json.loads((ROOT/'config/catalog.json').read_text())
    checks=[];failures=[]
    for r in catalog['records']:
        raw,rate=sf.read(ROOT/r['rawPath'],dtype='float32')
        audio,sr=sf.read(ROOT/r['listeningPath'],dtype='float32')
        valid=bool(len(raw)>rate and np.isfinite(raw).all() and np.isfinite(audio).all() and np.max(np.abs(audio))<.81 and np.sqrt(np.mean(audio**2))>.001 and rate==r['nativeSampleRate'] and sr==48000 and abs(len(raw)/rate-len(audio)/sr)<.005)
        # Re-measure the delivered listening WAV, rather than trusting normalization settings.
        proc=subprocess.run(['ffmpeg','-hide_banner','-nostdin','-i',str(ROOT/r['listeningPath']),'-af','loudnorm=I=-20:TP=-2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
        measured=json.loads(proc.stderr[proc.stderr.rfind('{'):proc.stderr.rfind('}')+1])
        loud=float(measured['input_i']);truepeak=float(measured['input_tp'])
        valid=valid and abs(loud+20)<=.5 and truepeak<=-1.8
        rms=np.sqrt(np.mean(audio.reshape(-1)**2))
        last=np.sqrt(np.mean(audio[-min(len(audio),round(.02*sr)):]**2))
        record=dict(model=r['model'],voice=r['voice'],test=r['test'],variant=r['variant'],valid=valid,nativeRate=rate,listeningRate=sr,seconds=len(audio)/sr,integratedLufs=loud,truePeakDbtp=truepeak,samplePeak=float(np.max(np.abs(audio))),rms=float(rms),last20msRms=float(last),wordTimingsVerified=False)
        checks.append(record)
        if not valid: failures.append(record)
    result=dict(checks=checks,failures=failures,subjectiveListeningPerformed=False,notes=['Waveform integrity, loudness, peak, rate and duration are measured.','Naturalness, pronunciation, sentence completion and breath quality need user listening.','Endpoint RMS is diagnostic; it cannot prove that the last word is intact.'])
    (ROOT/'config/audio-qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(f'{len(checks)} delivered listening WAVs checked; {len(failures)} failures; LUFS {min(c["integratedLufs"] for c in checks):.2f}..{max(c["integratedLufs"] for c in checks):.2f}; max true peak {max(c["truePeakDbtp"] for c in checks):.2f} dBTP')
    if failures: raise SystemExit(1)
if __name__=='__main__': main()
