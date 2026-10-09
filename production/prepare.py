"""Synthesize once, then align real audio offline. Never runs during a render."""
import argparse,json,subprocess,sys
from pathlib import Path
from core import ROOT,paths,read,write,spoken,bindings,export
sys.path.insert(0,str(ROOT/'tts'))
from cli import run_jobs
from benchmark import normalize

def main():
    p=argparse.ArgumentParser();p.add_argument('--id',required=True);group=p.add_mutually_exclusive_group();group.add_argument('--realign',action='store_true');group.add_argument('--audio',type=Path);a=p.parse_args()
    specpath,dest=paths(a.id);spec=read(specpath);config=read(ROOT/'tts/config/narrator.json')
    if config['activeModel']!='supertonic-3' or config['settings']['supertonic-3']!={'voice':'M1','speed':1.0}:raise ValueError('Expected user-selected M1 natural speed')
    if (dest/'narration.wav').exists() and not a.realign:raise ValueError('Assets exist. Use a new revision ID or --realign for unchanged audio.')
    dest.mkdir(parents=True,exist_ok=True)
    if a.audio:
        if spec.get('format')!='voice-test' or not spec.get('audioSource',{}).get('provider'):raise ValueError('Imported audio requires an explicit draft-only voice-test and audioSource provider')
        from import_audio import import_audio
        import_audio(a.audio,dest,spec['audioSource'])
        write(dest/'audio-bindings.json',bindings(specpath,dest/'narration.wav'))
    elif not a.realign:
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
