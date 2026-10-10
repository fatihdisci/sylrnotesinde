import sys,tempfile,unittest,json
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import local_voice,core

class EpisodeLocalVoiceTests(unittest.TestCase):
 def spec(self):return {'audioSource':{'provider':'local:antalia-mini'},'narrationSettings':{'model':'antalia-mini','voice':'default','speed':1,'seed':42},'phrases':[{'spoken':'Dünya iki milimetre.'}]}
 def test_requires_explicit_matching_model_and_keeps_m1_outside_this_path(self):
  for model in ['supertonic-3','ema-lightning','antalia-1']:
   with self.assertRaisesRegex(ValueError,'must agree'):local_voice.synthesize_local('test',self.spec(),model)
  s=self.spec();s['narrationSettings']['speed']=1.2
  with self.assertRaisesRegex(ValueError,'natural/1.05'):local_voice.synthesize_local('test',s,'antalia-mini')
 def test_existing_master_is_reused_without_model_call_and_changed_text_rejected(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);native=root/'tts/outputs/episodes/test/narration.wav';native.parent.mkdir(parents=True);native.write_bytes(b'48k fixture')
   config=root/'tts/config/models.json';config.parent.mkdir(parents=True);core.write(config,{'antalia-mini':{'revision':'pinned','package':'antalia-mini==1.0.0'}})
   lock=root/'tts/locks/antalia-mini.txt';lock.parent.mkdir(parents=True);lock.write_text('fixture')
   record={'model':'antalia-mini','voice':'default','speed':1,'seed':42,'text':'Dünya iki milimetre.','nativeSampleRate':48000,'offline':True,'networkAttempts':[]};core.write(native.with_suffix('.json'),record)
   with patch.object(local_voice,'ROOT',root):
    source,generation=local_voice.synthesize_local('test',self.spec(),'antalia-mini')
    self.assertEqual(source,native);self.assertEqual(generation['masterSha256'],core.sha(native.read_bytes()))
    bad=self.spec();bad['phrases'][0]['spoken']='Dünya üç milimetre.'
    with self.assertRaisesRegex(ValueError,'Existing master differs'):local_voice.synthesize_local('test',bad,'antalia-mini')
    record['offline']=False;core.write(native.with_suffix('.json'),record)
    with self.assertRaisesRegex(ValueError,'offline48kHz'):local_voice.synthesize_local('test',self.spec(),'antalia-mini')
if __name__=='__main__':unittest.main()
