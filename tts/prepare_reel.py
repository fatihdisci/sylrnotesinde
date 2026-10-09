"""Prepare twelve real profiles with the same short sentence, before video rendering."""
import array, json, math, shutil, subprocess, sys
from pathlib import Path
from cli import ROOT, MODELS, run_jobs
from benchmark import normalize
TEXT='Küçük bir fark, ölçek değiştiğinde bambaşka bir dünyaya dönüşebilir.'

def main():
    public=ROOT.parent/'public/tts-voice-reel';public.mkdir(parents=True,exist_ok=True)
    clips=[];from_frame=0
    for model,spec in MODELS.items():
        jobs=[dict(model=model,voice=voice,text=TEXT,speed=1.,seed=42,test='mobile-reel',variant='original',output=str(ROOT/'outputs/mobile-reel'/model/voice/'sentence.wav')) for voice in spec['voices']]
        missing=[j for j in jobs if not Path(j['output']).exists()]
        if missing: run_jobs(missing,os_offline=sys.platform=='darwin')
        for job in jobs:
            meta=normalize(Path(job['output']))
            source=ROOT/meta['listeningPath']
            audio=f'{model}-{job["voice"]}.wav';shutil.copy2(source,public/audio)
            pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(source),'-f','f32le','-ac','1','-ar','48000','-'])
            samples=array.array('f');samples.frombytes(pcm)
            if sys.byteorder!='little':samples.byteswap()
            peaks=[]
            for i in range(160):
                start=len(samples)*i//160;end=len(samples)*(i+1)//160
                peaks.append(round(max(abs(v) for v in samples[start:end]),5))
            length=math.ceil(meta['durationSeconds']*30)
            clip=dict(model=model,name=spec['name'],voice=job['voice'],audio='tts-voice-reel/'+audio,fromFrame=from_frame,durationInFrames=length+30,audioFrames=length,seconds=meta['durationSeconds'],peaks=peaks)
            clips.append(clip);from_frame+=clip['durationInFrames']
    manifest=dict(text=TEXT,fps=30,clips=clips,durationInFrames=from_frame+45)
    (ROOT/'comparison/reel-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(f'{len(clips)} voices, {manifest["durationInFrames"]/30:.2f} seconds incl canonical outro.')
if __name__=='__main__':main()
