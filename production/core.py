"""Shared timing, provenance and export rules. No inference, network or guessed word timing."""
import hashlib,json,math,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(data):return hashlib.sha256(data).hexdigest()
def read(path):return json.loads(Path(path).read_text())
def write(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');temp.replace(path)
def paths(id):
    if not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',id):raise ValueError('Invalid episode ID')
    return ROOT/f'src/episodes/{id}/production.json',ROOT/f'public/episodes/{id}'
def spoken(spec):return ' '.join(p['spoken'].strip() for p in spec['phrases'])
def bindings(specpath,audio):
    spec=read(specpath)
    return {'specHash':sha(Path(specpath).read_bytes()),'textHash':sha(spoken(spec).encode()),'settingsHash':sha((ROOT/'tts/config/narrator.json').read_bytes()),'ttsModelHash':sha((ROOT/'tts/config/models.json').read_bytes()),'audioHash':sha(Path(audio).read_bytes())}
def duration(path):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(path)]))
def timeline(seconds,start=0,hold=60,minimum=1200,speech_end_seconds=None):
    for n in [start,hold,minimum]:
        if type(n)!=int or n<0:raise ValueError('Timeline frames must be nonnegative integers')
    audio_frames=math.ceil(seconds*30)
    speech_frames=audio_frames if speech_end_seconds is None else math.ceil(speech_end_seconds*30)
    if not 0<speech_frames<=audio_frames:raise ValueError('Invalid measured speech end')
    content=max(minimum-45,start+audio_frames,start+speech_frames+hold)
    if content+45>1350:raise ValueError(f'{seconds:.3f}s narration plus result/outro exceeds45s. Simplify text first; M1 speed is unchanged.')
    return {'audioFrames':audio_frames,'narrationStartFrame':start,'resultFromFrame':start+speech_frames,'resultHoldFrames':content-start-speech_frames,'outroFromFrame':content,'durationInFrames':content+45}
def spec_timeline(data, spec):
    study = spec.get('format') == 'motion-study'
    minimum=spec.get('minimumDurationFrames',360) if study else 1200
    if study and (type(minimum)!=int or not 360<=minimum<=450):raise ValueError('MotionStudy minimum must be360–450 frames')
    t = timeline(data['audioDurationMs']/1000, spec.get('narrationStartFrame',0),
                 spec.get('resultHoldFrames',60), minimum=minimum,
                 speech_end_seconds=data['words'][-1]['endMs']/1000)
    if study and t['durationInFrames'] > 450:
        raise ValueError('MotionStudy exceeds15s; simplify speech, never change narrator speed')
    return t

def word_errors(data):
    errors=[];words=data.get('words',[]);expected=spoken(data['script']).split()
    if not words or [w['word'] for w in words]!=expected:errors.append('Missing/changed spoken words')
    if [w.get('id') for w in words]!=list(range(len(words))):errors.append('Missing/reordered word IDs')
    end=0
    for i,w in enumerate(words):
        a,b=w.get('startMs'),w.get('endMs')
        if not all(isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) for v in [a,b]) or not 0<=a<b<=data['audioDurationMs'] or a<end:
            errors.append(f'Invalid/overlapping word {i}');continue
        if b-a>2200:errors.append(f'Implausibly long word {i}')
        end=b
    # Re-check measured audio energy after manual edits as well as automatic alignment.
    energy=data.get('energy20ms',[])
    for left,right in zip(words,words[1:]):
        a,b=left.get('endMs',0),right.get('startMs',0)
        if not isinstance(a,(int,float)) or not isinstance(b,(int,float)) or not math.isfinite(a+b):continue
        if b-a>300 and energy:
            bins=energy[math.ceil(a/20):math.floor(b/20)]
            if bins and sum(v>.015 for v in bins)/len(bins)>.3:errors.append(f'Unexplained speech gap after word {left["id"]}')
    return errors
def verify_current(id,release=False):
    specpath,dest=paths(id);data=read(dest/'word-timings.json');manifest=read(dest/'narration-manifest.json')
    if data['bindings']!=bindings(specpath,dest/'narration.wav'):raise ValueError('STALE: text/audio/model settings changed; regenerate audio/alignment')
    if data['alignerHash']!=sha((ROOT/'alignment/model.json').read_bytes()):raise ValueError('STALE alignment model')
    if any(manifest['provenance'].get(k)!=v for k,v in data['bindings'].items()):raise ValueError('STALE manifest bindings')
    if manifest['provenance']['captionsHash']!=sha((dest/'captions.json').read_bytes()) or manifest['captions']!=read(dest/'captions.json'):raise ValueError('STALE captions')
    if manifest['provenance']['alignmentHash']!=sha((dest/'word-timings.json').read_bytes()):raise ValueError('STALE caption export; export corrected timings')
    spec=read(specpath)
    if data['script']!=spec:raise ValueError('STALE embedded script')
    schedule=spec_timeline(data,spec) if data.get('words') else None
    if manifest.get('timeline')!=schedule or manifest['durationInFrames']!=schedule['durationInFrames']:raise ValueError('Timeline does not match measured audio/hold')
    if abs(duration(dest/'narration.wav')*1000-data['audioDurationMs'])>1:raise ValueError('Audio duration mismatch')
    narration=manifest['narration']
    if len(narration)!=1 or narration[0]!={'id':'narration','text':spoken(spec),'from':schedule['narrationStartFrame'],'durationInFrames':schedule['audioFrames'],'path':f'episodes/{id}/narration.wav'}:raise ValueError('Narration asset/timing mismatch')
    if [i for cue in manifest['captions'] for i in cue.get('wordIds',[])]!=list(range(len(data['words']))):raise ValueError('Missing caption words')
    if [c['lines'] for c in manifest['captions']]!=[p['display'] for p in spec['phrases']]:raise ValueError('Caption display mapping mismatch')
    for cue in manifest['captions']:
        words=[data['words'][i] for i in cue['wordIds']]
        onset=(cue['from']-schedule['narrationStartFrame'])*1000/30
        offset=(cue['to']-schedule['narrationStartFrame'])*1000/30
        if abs(onset-words[0]['startMs'])>1000/30+.01 or not 0<=offset-words[-1]['endMs']<=1000/30+.01:raise ValueError('Caption does not match measured words')
    errors=word_errors(data)
    if errors:raise ValueError('; '.join(errors))
    if release and any(not gap.get('reviewed') for gap in data.get('unexplainedSpeechGaps',[])):raise ValueError('PUBLICATION BLOCKED: unexplained speech gaps')
    if release and (data['review']['status']!='approved' or not data['review'].get('reviewer') or not data['review'].get('listened') or any(w['reviewStatus']!='approved' for w in data['words'])):raise ValueError('PUBLICATION BLOCKED: human audio/timing review is not approved')
    return data,manifest

def export(id):
    specpath,dest=paths(id);data=read(dest/'word-timings.json');spec=read(specpath)
    if data['bindings']!=bindings(specpath,dest/'narration.wav'):raise ValueError('STALE sources')
    errors=word_errors(data)
    if errors:raise ValueError('; '.join(errors))
    t=spec_timeline(data,spec)
    cues=[];offset=0
    for phrase in spec['phrases']:
        count=len(phrase['spoken'].split());ws=data['words'][offset:offset+count]
        if not 1<=len(phrase['display'])<=2 or any(not line.strip() for line in phrase['display']):raise ValueError('Caption must have1–2 nonempty lines')
        # Floor onset, ceil offset. At30fps no spoken word loses its last frame.
        a=math.floor(ws[0]['startMs']*.03)+t['narrationStartFrame'];b=math.ceil(ws[-1]['endMs']*.03)+t['narrationStartFrame']
        if cues and a<cues[-1]['to']:a=cues[-1]['to'] # Quantization only, never alter measured word data.
        if a>=b:raise ValueError('Caption collapsed during frame quantization')
        cues.append({'from':a,'to':b,'lines':phrase['display'],'wordIds':list(range(offset,offset+count)),'timingSource':'forced-alignment'})
        offset+=count
    # Split long pauses within a phrase: author must supply meaningful shorter phrases.
    for cue in cues:
        ws=[data['words'][i] for i in cue['wordIds']]
        if any(b['startMs']-a['endMs']>750 for a,b in zip(ws,ws[1:])):raise ValueError('Long pause within caption: split the phrase in production.json and regenerate')
    write(dest/'captions.json',cues)
    def stamp(frame):
        ms=round(frame*1000/30);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
    (dest/'captions.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['from'])} --> {stamp(c['to'])}\n"+'\n'.join(c['lines']) for i,c in enumerate(cues))+'\n')
    provenance={**data['bindings'],'alignmentHash':sha((dest/'word-timings.json').read_bytes()),'captionsHash':sha((dest/'captions.json').read_bytes()),'reviewStatus':data['review']['status'],'reviewer':data['review'].get('reviewer'),'wordTimingPath':f'episodes/{id}/word-timings.json'}
    episode={'id':id,'title':spec['title'],'hook':spec['hook'],'brandVersion':'0.1-candidate','kind':'motion-study' if spec.get('format')=='motion-study' else 'episode','durationInFrames':t['durationInFrames'],'narration':[{'id':'narration','text':spoken(spec),'from':t['narrationStartFrame'],'durationInFrames':t['audioFrames'],'path':f'episodes/{id}/narration.wav'}],'sources':spec['sources'],'claims':spec['claims'],'scenes':spec.get('scenes') or [{'id':'continuous','from':0,'to':t['outroFromFrame'],'purpose':'Original continuous TSX visualization'}],'audio':{'voiceProvider':'local:supertonic-3','voiceStatus':'final' if data['review']['status']=='approved' else 'temporary'},'subtitlePath':f'episodes/{id}/captions.json','captions':cues,'provenance':provenance,'timeline':t,'fps':30,'captionReviewRequired':data['review']['status']!='approved','recommendedTotalFrames':t['durationInFrames']}
    write(dest/'narration-manifest.json',episode)
    print(f'Exported {len(data["words"])} words / {len(cues)} cues; {t["durationInFrames"]}/30s; review={data["review"]["status"]}',flush=True)
    return episode
