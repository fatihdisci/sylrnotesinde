"""Input failures must happen without loading a model or rewriting a recording."""
import subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ADAPTER=ROOT/'tts/adapters/chatterbox_v3.py'

class ChatterboxSafetyTests(unittest.TestCase):
 def test_existing_recording_is_never_overwritten(self):
  with tempfile.TemporaryDirectory() as directory:
   output=Path(directory)/'keep.wav';output.write_bytes(b'original recording')
   result=subprocess.run([sys.executable,str(ADAPTER),'--text','Güneş.','--output',str(output)],capture_output=True,text=True)
   self.assertNotEqual(result.returncode,0)
   self.assertIn('Output exists',result.stderr)
   self.assertEqual(output.read_bytes(),b'original recording')
 def test_ambiguous_text_sources_fail_before_model_loading(self):
  with tempfile.TemporaryDirectory() as directory:
   output=Path(directory)/'absent.wav'
   result=subprocess.run([sys.executable,str(ADAPTER),'--text','Güneş.','--text-file','nonexistent.txt','--output',str(output)],capture_output=True,text=True)
   self.assertNotEqual(result.returncode,0)
   self.assertIn('Supply text or text-file',result.stderr)
   self.assertFalse(output.exists())
if __name__=='__main__':unittest.main()
