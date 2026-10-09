"""Prepare narration assets before Remotion. Does not edit any existing episode or brand."""
import argparse, hashlib, json, math, re, shutil, sys
from pathlib import Path
from cli import ROOT, MODELS, run_jobs
from benchmark import normalize

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--id',required=True,help='New episode ID; existing assets are not overwritten')
    p.add_argument('--text-file',required=True)
    p.add_argument('--model',choices=list(MODELS))
    p.add_argument('--voice');p.add_argument('--speed',type=float)
    p.add_argument('--captions',help='Optional hand-checked JSON cues: [{from,to,lines:[...]}], in frames')
    p.add_argument('--allow-extended-duration',action='store_true',help='Explicitly allow narration outside 38.5–43.5 seconds')
    a=p.parse_args()
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',a.id): p.error('ID must be lowercase ASCII words separated by hyphens')
    config=json.loads((ROOT/'config/narrator.json').read_text())
    model=a.model or config['activeModel']
    if not model: p.error('No narrator selected. Supply --model explicitly or wait for the user decision.')
    settings=config['settings'][model]
    dest=ROOT.parent/'public/episodes'/a.id
    if dest.exists(): p.error('Episode asset folder already exists; create a new revision ID to preserve it.')
    text=Path(a.text_file).read_text().strip()
    if not text: p.error('Empty narration')
    job=dict(model=model,voice=a.voice or settings['voice'],speed=a.speed if a.speed is not None else settings['speed'],text=text,seed=config['seed'],test='episode',variant='original',output=str(ROOT/'outputs/episodes'/a.id/'narration.wav'))
    run_jobs([job],device=config['device'],os_offline=sys.platform=='darwin')
    metadata=normalize(Path(job['output']))
    frames=math.ceil(metadata['durationSeconds']*30)
    if not a.allow_extended_duration and not 1155<=frames<=1305:
        p.error(f'Generated {metadata["durationSeconds"]:.2f}s narration; adjust text/native speed before export. Master preserved in tts/outputs/episodes/{a.id}/.')
    cues=json.loads(Path(a.captions).read_text()) if a.captions else []
    previous=0
    for cue in cues:
        if not (isinstance(cue.get('from'),int) and isinstance(cue.get('to'),int) and previous<=cue['from']<cue['to']<=frames and isinstance(cue.get('lines'),list) and 1<=len(cue['lines'])<=2 and all(isinstance(s,str) for s in cue['lines'])): p.error('Invalid caption range, overlap or line count')
        previous=cue['to']
    dest.mkdir(parents=True)
    shutil.copy2(ROOT/metadata['listeningPath'],dest/'narration.wav')
    cue_path=f'episodes/{a.id}/captions.json'
    (dest/'captions.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2)+'\n')
    output=dict(id=a.id,brandVersion='0.1-candidate',fps=30,narration=[dict(id='narration',text=text,from_=0,durationInFrames=frames,path=f'episodes/{a.id}/narration.wav')],audio=dict(voiceProvider=f'local:{model}',voiceStatus='temporary'),subtitlePath=cue_path,captions=cues,wordTimingSource='EMA model 40ms grid' if metadata['words'] else 'none',wordTimingsVerified=False,captionReviewRequired=not bool(a.captions),recommendedTotalFrames=max(1200,frames+45),metadata=metadata)
    output['narration'][0]['from']=output['narration'][0].pop('from_')
    (dest/'narration-manifest.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(f'Prepared {dest}; total minimum incl. canonical outro: {output["recommendedTotalFrames"]}/30 seconds.')
    print('Import narration/audio/subtitlePath/captions into the new typed Episode. Review captions before rendering.')

if __name__=='__main__': main()
