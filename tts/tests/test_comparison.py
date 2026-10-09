import importlib.util, json, tempfile, unittest, threading, urllib.request, urllib.error
from pathlib import Path
MODULE=Path(__file__).resolve().parents[1]/'comparison/server.py'
spec=importlib.util.spec_from_file_location('comparison_server',MODULE)
server=importlib.util.module_from_spec(spec);spec.loader.exec_module(server)

class ComparisonTests(unittest.TestCase):
    def test_rating_validation(self):
        valid=dict.fromkeys(server.DIMS,3)
        self.assertEqual(server.valid_rating(valid),valid)
        for bad in [{},dict.fromkeys(server.DIMS,6),dict.fromkeys(server.DIMS,True),dict.fromkeys(server.DIMS,1.5)]:
            with self.assertRaises(ValueError): server.valid_rating(bad)
    def test_blind_persistence_and_reveal_gate(self):
        with tempfile.TemporaryDirectory() as temp:
            session=server.Session(temp)
            public=json.dumps(session.public())
            for model in session.models.values(): self.assertNotIn(model['name'],public)
            self.assertFalse(session.complete())
            session.save(dict(id=session.required[0],ratings={'overall':4},comment='partial fixture'))
            self.assertFalse(session.complete())
            self.assertEqual(server.Session(temp).data['ratings'][session.required[0]]['scores'],{'overall':4})
            with self.assertRaises(ValueError): session.save([])
            with self.assertRaises(ValueError): session.save(dict(reveal=True))
            with self.assertRaises(ValueError): session.save(dict(id='../../escape',ratings=dict.fromkeys(server.DIMS,5)))
            with self.assertRaises(ValueError): session.save(dict(id=session.required[0],ratings=dict.fromkeys(server.DIMS,3),comment='x'*5001))
            for clip_id in session.required: session.save(dict(id=clip_id,ratings=dict.fromkeys(server.DIMS,3),comment='TEST FIXTURE'))
            self.assertTrue(session.complete())
            result=session.save(dict(reveal=True))
            self.assertTrue(result['revealed'])
            self.assertTrue(all(g['name'] for g in result['groups']))
            restored=server.Session(temp)
            self.assertEqual(restored.data,session.data)
            exported=json.loads(next((Path(temp)/'results').glob('*.json')).read_text())
            self.assertEqual(len(exported['ratings']),12)
            self.assertIn('identities',exported)
    def test_http_privacy_origin_and_audio_range(self):
        with tempfile.TemporaryDirectory() as temp:
            session=server.Session(temp)
            http=server.ThreadingHTTPServer(('127.0.0.1',0),server.handler(session))
            thread=threading.Thread(target=http.serve_forever,daemon=True);thread.start()
            base=f'http://127.0.0.1:{http.server_port}'
            try:
                with urllib.request.urlopen(base+'/api/session') as response:
                    payload=response.read().decode()
                    self.assertIn("connect-src 'self'",response.headers['Content-Security-Policy'])
                    for model in session.models.values(): self.assertNotIn(model['name'],payload)
                clip_id=next(iter(session.by_id))
                with urllib.request.urlopen(urllib.request.Request(base+'/audio/'+clip_id,headers={'Range':'bytes=0-43'})) as response:
                    self.assertEqual(response.status,206)
                    self.assertEqual(response.read()[:4],b'RIFF')
                    self.assertEqual(response.headers['Content-Length'],'44')
                for request in [urllib.request.Request(base+'/api/session',headers={'Host':'evil.example'}),urllib.request.Request(base+'/api/save',data=b'{}',headers={'Origin':'https://evil.example','Content-Type':'application/json'})]:
                    with self.assertRaises(urllib.error.HTTPError) as error: urllib.request.urlopen(request)
                    self.assertEqual(error.exception.code,403)
                    error.exception.close()
                with self.assertRaises(urllib.error.HTTPError) as error: urllib.request.urlopen(base+'/fonts/../../AGENTS.md')
                self.assertEqual(error.exception.code,404)
                error.exception.close()
            finally:
                http.shutdown();http.server_close();thread.join()

    def test_texts_and_all_voices_exist(self):
        with tempfile.TemporaryDirectory() as temp:
            session=server.Session(temp)
            self.assertEqual(len(session.records),72)
            self.assertEqual(len(session.required),12)
            for model,config in session.models.items():
                for voice in config['voices']:
                    for test in ['A','B','C','D']:
                        matches=[r for r in session.records if (r['model'],r['voice'],r['test'],r['variant'])==(model,voice,test,'original')]
                        self.assertEqual(len(matches),1)
                        self.assertTrue((server.ROOT/matches[0]['listeningPath']).exists())

if __name__=='__main__': unittest.main()
