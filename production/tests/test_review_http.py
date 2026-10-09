import json,subprocess,sys,unittest,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class LiveReviewHttpTests(unittest.TestCase):
    def test_real_audio_range_and_invalid_save_leave_artifacts_unchanged(self):
        if not (ROOT.parent/'public/episodes/production-check/narration.wav').exists():self.skipTest('Prepare integration fixture first')
        project=ROOT.parent;word=project/'public/episodes/production-check/word-timings.json';before=word.read_bytes()
        process=subprocess.Popen([sys.executable,str(ROOT/'review.py'),'--id','production-check','--port','3034'],cwd=project,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
        try:
            self.assertIn('3034',process.stdout.readline())
            base='http://127.0.0.1:3034'
            with urllib.request.urlopen(base+'/state') as response:data=json.load(response)
            with urllib.request.urlopen(urllib.request.Request(base+'/audio',headers={'Range':'bytes=0-43'})) as response:self.assertEqual(response.status,206);self.assertEqual(response.read()[:4],b'RIFF')
            with self.assertRaises(urllib.error.HTTPError) as error:urllib.request.urlopen(urllib.request.Request(base+'/state',headers={'Host':'evil.invalid'}))
            self.assertEqual(error.exception.code,403);error.exception.close()
            payload={'words':[{k:w[k] for k in ['id','startMs','endMs']} for w in data['words']],'expectedAlignmentHash':data['alignmentHash'],'approve':True,'listened':False,'reviewer':'TEST FIXTURE'}
            with self.assertRaises(urllib.error.HTTPError) as error:urllib.request.urlopen(urllib.request.Request(base+'/save',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'}))
            self.assertEqual(error.exception.code,400);self.assertIn('Listening',error.exception.read().decode());error.exception.close()
            self.assertEqual(word.read_bytes(),before)
        finally:
            process.terminate();process.wait(timeout=10);process.stdout.close()
if __name__=='__main__':unittest.main()
