"""Import supplied audio, then align locally. M1 is an explicit legacy option."""
import argparse,json,subprocess,sys
from pathlib import Path
from core import ROOT,paths,read,write,spoken,bindings,export
sys.path.insert(0,str(ROOT/'tts'))

def main():
    p=argparse.ArgumentParser();p.add_argument('--id',required=True);p.add_argument('--script',type=Path);group=p.add_mutually_exclusive_group(required=True);group.add_argument('--realign',action='store_true');group.add_argument('--audio',type=Path);group.add_argument('--synthesize-m1',action='store_true');group.add_argument('--synthesize-model',choices=['antalia-mini'],help='Explicit per-episode local narrator; preserves the global M1 selection');a=p.parse_args()
    specpath,dest=paths(a.id);spec=read(specpath)
    if a.audio and spec.get('format')=='audio-first' and not a.script:raise ValueError('Supply the exact finalized --script text file')
    if a.script:
        import unicodedata
        clean=lambda s:' '.join(unicodedata.normalize('NFC',s).split())
        if clean(a.script.read_text(encoding='utf-8'))!=clean(spoken(spec)):raise ValueError('Script differs from production phrases. Update the exact transcript first; timings must not be reused.')
    if (dest/'narration.wav').exists() and not a.realign:raise ValueError('Assets exist. Use a new revision ID or --realign for unchanged audio.')
    dest.mkdir(parents=True,exist_ok=True)
    if a.synthesize_model:
        from local_voice import synthesize_local
        from import_audio import import_audio
        source,generation=synthesize_local(a.id,spec,a.synthesize_model)
        import_audio(source,dest,spec['audioSource'],specpath.parent/'script.txt',generation=generation)
        write(dest/'audio-bindings.json',bindings(specpath,dest/'narration.wav'))
    elif a.audio:
        if not spec.get('audioSource',{}).get('provider'):raise ValueError('Imported audio requires an explicit audioSource provider')
        from import_audio import import_audio
        import_audio(a.audio,dest,spec['audioSource'],a.script)
        write(dest/'audio-bindings.json',bindings(specpath,dest/'narration.wav'))
    elif not a.realign:
        from cli import run_jobs
        from benchmark import normalize
        config=read(ROOT/'tts/config/narrator.json')
        if config['activeModel']!='supertonic-3' or config['settings']['supertonic-3']!={'voice':'M1','speed':1.0}:raise ValueError('Expected user-selected M1 natural speed')
        if spec.get('audioSource'):raise ValueError('External audio test requires --audio; M1 synthesis is not a substitute')
        native=ROOT/f'tts/outputs/episodes/{a.id}/narration.wav'
        (ROOT/'tts/outputs').mkdir(exist_ok=True)
        run_jobs([{'model':'supertonic-3','voice':'M1','text':spoken(spec),'speed':1.0,'seed':config['seed'],'output':str(native)}],device='cpu',os_offline=True)
        import shutil;metadata=normalize(native);shutil.copy2(ROOT/'tts'/metadata['listeningPath'],dest/'narration.wav')
        write(dest/'audio-bindings.json',bindings(specpath,dest/'narration.wav'))
    elif read(dest/'audio-bindings.json')!=bindings(specpath,dest/'narration.wav'):raise ValueError('STALE audio; changed text/settings require new synthesis with a new revision ID')
    executable=ROOT/'alignment/environments/ctc/bin/python'
    subprocess.run(['/usr/bin/sandbox-exec','-p','(version 1) (allow default) (deny network*)',str(executable),str(ROOT/'alignment/align.py'),'--id',a.id],check=True,cwd=ROOT)
    export(a.id)
if __name__=='__main__':main()
