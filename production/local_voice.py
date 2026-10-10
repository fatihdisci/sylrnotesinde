"""Explicit, episode-scoped local TTS. Never changes or sets up the M1 fallback."""
import sys
from core import ROOT,read,spoken,sha
sys.path.insert(0,str(ROOT/'tts'))

def synthesize_local(id,spec,model):
    settings=spec.get('narrationSettings',{})
    models=read(ROOT/'tts/config/models.json')
    if model!='antalia-mini' or settings.get('model')!=model or spec.get('audioSource',{}).get('provider')!=f'local:{model}':
        raise ValueError('Explicit episode model/settings/provider must agree')
    if settings.get('voice')!='default' or settings.get('speed') not in [1,1.05] or type(settings.get('seed'))!=int:
        raise ValueError('Antalia Mini requires default voice, reviewed natural/1.05 speed and fixed seed')
    native=ROOT/f'tts/outputs/episodes/{id}/narration.wav'
    job={'model':model,'voice':settings['voice'],'speed':settings['speed'],'seed':settings['seed'],'text':spoken(spec),'output':str(native)}
    if native.exists():
        record=read(native.with_suffix('.json'))
        if any(record.get(k)!=job[k] for k in ['model','voice','speed','seed','text']):raise ValueError('Existing master differs; preserve it and use a new revision ID')
    else:
        from cli import run_jobs
        run_jobs([job],device='cpu',os_offline=True)
        record=read(native.with_suffix('.json'))
    if record['nativeSampleRate']!=48000 or not record['offline'] or record['networkAttempts']:raise ValueError('Expected offline48kHz Antalia master')
    generation={k:v for k,v in record.items() if k not in ['output','text','words']}
    generation.update(modelRevision=models[model]['revision'],package=models[model]['package'],lockSha256=sha((ROOT/f'tts/locks/{model}.txt').read_bytes()),masterSha256=sha(native.read_bytes()),textSha256=sha(spoken(spec).encode()))
    return native,generation
