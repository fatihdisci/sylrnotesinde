"""Import a user-supplied recording locally; never synthesize or time-stretch it."""
import json,subprocess,shutil
from pathlib import Path
from core import ROOT,sha,write

def import_audio(source,dest,description,script=None):
    source=Path(source)
    if not source.is_file():raise ValueError('Audio input does not exist')
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(source)]))
    if not any(s['codec_type']=='audio' for s in probe['streams']):raise ValueError('Input has no audio stream')
    archive=ROOT/'voice-sources'/dest.name/('original'+source.suffix.lower())
    if archive.exists() and sha(archive.read_bytes())!=sha(source.read_bytes()):raise ValueError('Archived source differs; use a new episode revision')
    archive.parent.mkdir(parents=True,exist_ok=True)
    if not archive.exists():shutil.copy2(source,archive)
    analysis=subprocess.run(['ffmpeg','-hide_banner','-nostdin','-i',str(source),'-af','loudnorm=I=-20:TP=-2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    loud=json.loads(analysis.stderr[analysis.stderr.rfind('{'):analysis.stderr.rfind('}')+1])
    af='loudnorm=I=-20:TP=-2:LRA=11:linear=true:'+':'.join(f'{a}={loud[b]}' for a,b in [('measured_I','input_i'),('measured_TP','input_tp'),('measured_LRA','input_lra'),('measured_thresh','input_thresh'),('offset','target_offset')])
    dest.mkdir(parents=True,exist_ok=True)
    subprocess.run(['ffmpeg','-y','-v','error','-nostdin','-i',str(source),'-map','0:a:0','-af',af,'-ar','48000','-ac','1','-c:a','pcm_s24le',str(dest/'narration.wav')],check=True)
    metadata={'provider':description['provider'],'voice':description.get('voice','user-supplied'),'sourceFilename':source.name,'sourceSha256':sha(source.read_bytes()),'sourceDurationSeconds':float(probe['format']['duration']),'processing':'two-pass loudnorm -20 LUFS / -2 dBTP; 48 kHz mono PCM24; original timing retained','synthesisPerformed':False,'humanListeningPerformed':False}
    if script:
        shutil.copy2(script,dest/'script.txt')
        metadata.update(schemaVersion=2,archivePath=str(archive.relative_to(ROOT)),scriptSha256=sha((dest/'script.txt').read_bytes()))
    write(dest/'external-audio.json',metadata)
