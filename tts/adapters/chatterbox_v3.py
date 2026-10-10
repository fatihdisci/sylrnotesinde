"""Pinned local Chatterbox V3: Turkish, native sample rate, isolated environment."""
import argparse,json,os,sys,time,resource,hashlib,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HOME=str(ROOT/'tts/.cache/chatterbox'),NUMBA_CACHE_DIR=str(ROOT/'tts/.cache/chatterbox/numba'))

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--text');p.add_argument('--text-file',type=Path);p.add_argument('--output',type=Path,required=True)
 p.add_argument('--device',choices=['cpu','mps'],default='cpu');p.add_argument('--cfg',type=float);p.add_argument('--exaggeration',type=float)
 refs=p.add_mutually_exclusive_group();refs.add_argument('--reference',type=Path,help='Optional local, rights-cleared Turkish reference')
 refs.add_argument('--builtin-voice',action='store_true',help='Use official built-in conditionals instead of the configured project reference')
 p.add_argument('--allow-network',action='store_true',help='Setup diagnostics only; ordinary generation is offline')
 args=p.parse_args();args.output=args.output.resolve();config=json.loads((ROOT/'tts/config/chatterbox.json').read_text())
 if bool(args.text)==bool(args.text_file):raise ValueError('Supply text or text-file')
 if args.output.exists():raise ValueError('Output exists; choose a new candidate name')
 if ROOT not in args.output.parents:raise ValueError('Save generated audio inside this project')
 attempts=[]
 if not args.allow_network:
  def offline(event,values):
   if event in ('socket.connect','socket.getaddrinfo','socket.sendto'):
    attempts.append(event);raise PermissionError('Chatterbox generation is offline')
  sys.addaudithook(offline)
 import numpy as np,torch,soundfile as sf
 from chatterbox.mtl_tts import ChatterboxMultilingualTTS
 from chatterbox.models.tokenizers.tokenizer import ChineseCangjieConverter
 # Upstream eagerly initializes a Chinese-only downloader even for Turkish.
 # This adapter is tr-only: leave that unused converter inert, without changing
 # Turkish tokenization, model weights, vendor sources or any other environment.
 def turkish_only_converter(self,model_dir=None):
  self.word2cj={};self.cj2word={};self.segmenter=None
 ChineseCangjieConverter.__init__=turkish_only_converter
 torch.set_num_threads(config['threads']);torch.manual_seed(config['seed']);np.random.seed(config['seed'])
 start=time.perf_counter();cpu0=time.process_time()
 model=ChatterboxMultilingualTTS.from_local(ROOT/'tts/models/chatterbox',device=args.device,t3_model='v3')
 if model.conds is None:raise ValueError('Missing official built-in voice conditionals')
 settings={**config['settings']}
 if args.cfg is not None:settings['cfg_weight']=args.cfg
 if args.exaggeration is not None:settings['exaggeration']=args.exaggeration
 if not args.reference and not args.builtin_voice and config.get('reference'):
  args.reference=ROOT/config['reference']
 if args.reference:
  args.reference=args.reference.resolve()
  if ROOT not in args.reference.parents or not args.reference.is_file():raise ValueError('Reference must be an existing project-local recording')
  if args.reference==ROOT/config.get('reference','') and digest(args.reference)!=config['referenceSha256']:raise ValueError('Configured reference checksum changed')
  model.prepare_conditionals(str(args.reference),exaggeration=settings['exaggeration'])
 text=args.text or args.text_file.read_text(encoding='utf-8').strip()
 chunks=re.split(r'(?<=[.!?])\s+',text)
 args.output.parent.mkdir(parents=True,exist_ok=True);chunk_dir=args.output.parent/(args.output.stem+'-chunks');chunk_dir.mkdir(exist_ok=True)
 records=[];waves=[]
 for i,sentence in enumerate(chunks):
  torch.manual_seed(config['seed']+i);np.random.seed(config['seed']+i)
  began=time.perf_counter();wave=model.generate(sentence,language_id='tr',**settings).squeeze().numpy()
  if not np.isfinite(wave).all() or len(wave)<model.sr*.3:raise ValueError('Empty/corrupt generated speech')
  file=chunk_dir/f'{i:02d}.wav';sf.write(file,wave,model.sr,subtype='FLOAT')
  # Keep native sentence timing. No speed, pitch or pause manipulation.
  records.append({'index':i,'text':sentence,'file':str(file.relative_to(ROOT)),'sha256':digest(file),'durationSeconds':len(wave)/model.sr,'generationSeconds':time.perf_counter()-began,'fromSample':sum(len(w) for w in waves)})
  waves.append(wave);print(json.dumps(records[-1],ensure_ascii=False),flush=True)
 final=np.concatenate(waves);sf.write(args.output,final,model.sr,subtype='FLOAT')
 report={'model':config['model'],'codeRevision':config['codeRevision'],'modelRevision':config['modelRevision'],'voice':'project-local Turkish reference' if args.reference else 'official builtin conditionals','referencePath':str(args.reference.relative_to(ROOT)) if args.reference else None,'referenceSha256':digest(args.reference) if args.reference else None,'language':'tr','settings':settings,'seed':config['seed'],'device':args.device,'threads':config['threads'],'sampleRate':model.sr,'nativeSampleRate':model.sr,'seconds':len(final)/model.sr,'generationSeconds':time.perf_counter()-start,'cpuSeconds':time.process_time()-cpu0,'peakResidentBytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'audioSha256':digest(args.output),'textSha256':hashlib.sha256(text.encode()).hexdigest(),'chunks':records,'networkAttempts':attempts,'offlineGeneration':not args.allow_network,'humanListeningPerformed':False,'postPitchOrSpeedProcessing':False,'compatibility':'Turkish-only adapter bypasses unused eager Chinese Cangjie/pkuseg initialization'}
 args.output.with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='chunks'},indent=2),flush=True)
if __name__=='__main__':main()
