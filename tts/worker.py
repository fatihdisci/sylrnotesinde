"""Private inference process: one isolated venv; socket access denied before imports."""
import argparse, json, os, sys, time, threading
from pathlib import Path
ROOT = Path(__file__).resolve().parent
os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1', HF_HOME=str(ROOT/'.cache/hf'), XDG_CACHE_HOME=str(ROOT/'.cache'), OMP_NUM_THREADS='2', TOKENIZERS_PARALLELISM='false')
network_attempts=[]
def deny_network(event, args):
    if event in ('socket.connect', 'socket.getaddrinfo', 'socket.sendto'):
        network_attempts.append(event)
        raise PermissionError('TTS inference is offline: network access denied')
sys.addaudithook(deny_network)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--jobs', required=True)
    parser.add_argument('--device', default='cpu', choices=['cpu','mps'])
    args=parser.parse_args()
    import psutil, numpy as np, soundfile as sf
    from adapters.local import ADAPTERS
    jobs=json.loads(Path(args.jobs).read_text())
    process=psutil.Process()
    peak=[process.memory_info().rss]
    stop=threading.Event()
    def monitor():
        while not stop.wait(.02): peak[0]=max(peak[0], process.memory_info().rss)
    threading.Thread(target=monitor,daemon=True).start()
    start=time.perf_counter()
    engine=ADAPTERS[jobs[0]['model']](args.device)
    load=time.perf_counter()-start
    for job in jobs:
        peak[0]=process.memory_info().rss
        before=process.cpu_times(); started=time.perf_counter()
        audio, rate, words, normalized=engine.generate(job['text'],job['voice'],job.get('speed',1.),job.get('seed',42))
        elapsed=time.perf_counter()-started
        after=process.cpu_times()
        cpu=(after.user+after.system)-(before.user+before.system)
        audio=np.asarray(audio,dtype=np.float32).reshape(-1)
        if not len(audio) or not np.isfinite(audio).all() or np.max(np.abs(audio))<.00001:
            raise ValueError('Empty, non-finite or silent inference')
        output=Path(job['output']); output.parent.mkdir(parents=True,exist_ok=True)
        # FLOAT master preserves the model's native samples, even if a model exceeds full scale.
        sf.write(output,audio,rate,subtype='FLOAT')
        record={**job,'device':args.device,'nativeSampleRate':rate,'durationSeconds':len(audio)/rate,'generationSeconds':elapsed,'modelLoadSeconds':load,'cpuSeconds':cpu,'meanCpuPercent':100*cpu/elapsed,'peakRssMiB':peak[0]/1024**2,'realtimeFactor':elapsed/(len(audio)/rate),'rawPeak':float(np.max(np.abs(audio))),'words':words,'wordTimingsVerified':False,'modelNormalizedText':normalized,'offline':True,'networkAttempts':list(network_attempts),'threads':2}
        output.with_suffix('.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({k:record[k] for k in ['model','voice','durationSeconds','generationSeconds','peakRssMiB']},ensure_ascii=False),flush=True)
    stop.set()

if __name__=='__main__': main()
