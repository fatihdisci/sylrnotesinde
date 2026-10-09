"""Resolve authored meaning to measured words. Shared by scenes, effects and review."""
import argparse,json,math
from core import paths,read,write,sha

def resolve_storyboard(path,data,timeline):
    board=read(path);words=data['words'];offset=timeline['narrationStartFrame'];end=timeline['outroFromFrame']
    def anchor(a):
        if a=='start':return 0
        if a=='outro':return end
        w=words[a['word']]
        if w['word']!=a['text']:raise ValueError(f'Storyboard word changed: {a}')
        ms=w['endMs'] if a.get('edge')=='end' else w['startMs']
        f=(math.ceil(ms*.03) if a.get('edge')=='end' else math.floor(ms*.03))+offset+a.get('offsetFrames',0)
        if not 0<=f<=end:raise ValueError('Storyboard event outside content')
        return f
    events=[]
    for item in board['events']:
        event={**item,'from':anchor(item['at']),'to':anchor(item.get('until','outro'))}
        if event['to']<=event['from']:raise ValueError('Empty storyboard event')
        event['effects']=[{**effect,'frame':event['from']+effect.get('offsetFrames',0)} for effect in item.get('effects',[])]
        if any(e['frame']<0 or e['frame']+e['durationFrames']>end for e in event['effects']):raise ValueError('Effect crosses content boundary')
        event['captions']=[p['display'] for p,m in zip(data['script']['phrases'],data['displayMap']) if words[m['spokenWordIds'][0]]['startMs']*.03+offset<event['to'] and words[m['spokenWordIds'][-1]]['endMs']*.03+offset>event['from']]
        events.append(event)
    if len({e['id'] for e in events})!=len(events):raise ValueError('Duplicate event ID')
    if [e['from'] for e in events]!=sorted(e['from'] for e in events):raise ValueError('Events must follow narration order')
    phrases=[]
    for i,m in enumerate(data['displayMap']):
        ws=[words[j] for j in m['spokenWordIds']]
        phrases.append({'id':i,'fromMs':ws[0]['startMs'],'toMs':ws[-1]['endMs'],'spoken':' '.join(w['word'] for w in ws),'pauseAfterMs':max(0,words[ws[-1]['id']+1]['startMs']-ws[-1]['endMs']) if ws[-1]['id']+1<len(words) else 0})
    return {'schemaVersion':1,'idea':board['idea'],'storyboardHash':sha(path.read_bytes()),'events':events,'speech':{'onsetMs':words[0]['startMs'],'offsetMs':words[-1]['endMs'],'audioDurationMs':data['audioDurationMs'],'phrases':phrases,'listeningVerified':False}}

def write_storyboard(dest,direction):
    write(dest/'storyboard.json',direction)
    rows=['# Ses temelli storyboard','',direction['idea'],'','Zamanlar gerçek WAV kelimelerinden üretilir. İnsan dinleme onayı değildir.','','| Zaman | Bilgi | Görsel olay | Kamera / hareket | Efekt | Altyazı |','|---|---|---|---|---|---|']
    for e in direction['events']:
        rows.append(f"| {e['from']/30:.3f}–{e['to']/30:.3f} s | {e['information']} | {e['visual']} | {e['camera']} · {e['animation']} | {', '.join(x['sound'] for x in e['effects']) or '—'} | {' / '.join(' '.join(c) for c in e['captions'])} |")
    (dest/'storyboard.md').write_text('\n'.join(rows)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--id',required=True);a=p.parse_args()
    from core import export
    spec,_=paths(a.id)
    if not (spec.parent/'storyboard.json').exists():raise ValueError('Author storyboard.json with measured-word anchors first')
    export(a.id)
