import os,copy,json,sys,tempfile,unittest,shutil
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import core,review

class ProductionTests(unittest.TestCase):
    def sample(self):
        return {'script':{'phrases':[{'spoken':'Ölçek değişir.','display':['Ölçek değişir.']}]},'audioDurationMs':1800,'words':[{'id':0,'word':'Ölçek','startMs':200,'endMs':700,'confidence':.9,'reviewStatus':'automatic','corrections':[]},{'id':1,'word':'değişir.','startMs':850,'endMs':1500,'confidence':.9,'reviewStatus':'automatic','corrections':[]}],'unexplainedSpeechGaps':[],'review':{'status':'needs_review'}}
    def test_total_duration_includes_hold_once(self):
        t=core.timeline(37.5,hold=60)
        self.assertEqual(t['durationInFrames'],1230)
        self.assertEqual(t['resultHoldFrames'],60)
        self.assertEqual(t['outroFromFrame'],1185)
        self.assertEqual(core.timeline(33,hold=60)['durationInFrames'],1200)
        self.assertEqual(core.timeline(42,hold=60,speech_end_seconds=40.8)['durationInFrames'],1329)
        for args in [(44,0,60),(37,-1,60),(37,0,1.5)]:
            with self.assertRaises(ValueError):core.timeline(*args)
    def test_motion_study_duration_cannot_weaken_episode_contract(self):
        data={'audioDurationMs':12510,'words':[{'endMs':12000}]}
        self.assertEqual(core.spec_timeline(data,{'format':'motion-study','minimumDurationFrames':450,'resultHoldFrames':36})['durationInFrames'],450)
        self.assertEqual(core.spec_timeline(data,{'minimumDurationFrames':450})['durationInFrames'],1200)
        for value in [359,451,450.5,True]:
            with self.assertRaises(ValueError):core.spec_timeline(data,{'format':'motion-study','minimumDurationFrames':value})
        with self.assertRaises(ValueError):core.spec_timeline({'audioDurationMs':14500,'words':[{'endMs':14000}]},{'format':'motion-study'})

    def test_word_identity_missing_overlap_and_invalid_values(self):
        self.assertEqual(core.word_errors(self.sample()),[])
        for edit in [lambda d:d['words'].pop(),lambda d:d['words'][1].update(startMs=600),lambda d:d['words'][0].update(endMs=-1),lambda d:d['words'][1].update(endMs=float('nan')),lambda d:d['words'][0].update(startMs=True),lambda d:d['words'][1].update(word='başka'),lambda d:d['words'][1].update(id=7)]:
            d=self.sample();edit(d);self.assertTrue(core.word_errors(d))
    def test_speech_energy_rejects_unexplained_holes(self):
        data=self.sample();data['words'][1]['startMs']=1100;data['energy20ms']=[.1]*90
        self.assertTrue(any('speech gap' in e for e in core.word_errors(data)))
        data['energy20ms']=[0.]*90;self.assertEqual(core.word_errors(data),[])

    def test_hash_changes_for_text_audio_and_settings(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'tts/config').mkdir(parents=True)
            config=root/'tts/config/narrator.json';config.write_text('{}');(root/'tts/config/models.json').write_text('{}')
            spec=root/'spec.json';spec.write_text(json.dumps(self.sample()['script']));audio=root/'a.wav';audio.write_bytes(b'fixture-audio')
            with patch.object(core,'ROOT',root):
                first=core.bindings(spec,audio);audio.write_bytes(b'changed');self.assertNotEqual(first['audioHash'],core.bindings(spec,audio)['audioHash']);config.write_text('{"speed":1}');self.assertNotEqual(first['settingsHash'],core.bindings(spec,audio)['settingsHash']);spec.write_text(json.dumps({'phrases':[{'spoken':'Yeni metin.'}]}));self.assertNotEqual(first['textHash'],core.bindings(spec,audio)['textHash'])
    def test_publication_hash_gate_on_real_isolated_assets(self):
        fixture_id=os.environ.get('EPISODE_TEST_ID','production-check')
        source=core.ROOT/f'public/episodes/{fixture_id}'
        if not (source/'narration.wav').exists():self.skipTest('Prepare integration audio first')
        with tempfile.TemporaryDirectory() as directory:
            dest=Path(directory)
            for name in ['narration.wav','word-timings.json','captions.json','captions.srt','narration-manifest.json']:shutil.copy2(source/name,dest/name)
            spec=core.ROOT/f'src/episodes/{fixture_id}/production.json'
            with patch.object(core,'paths',return_value=(spec,dest)):
                self.assertEqual(core.verify_current(fixture_id)[0]['review']['status'],'needs_review')
                with self.assertRaisesRegex(ValueError,'PUBLICATION BLOCKED'):core.verify_current(fixture_id,True)
                # Simulate approval only in disposable TEST FIXTURE data; never user artifacts.
                data=core.read(dest/'word-timings.json');data['review']={'status':'approved','reviewer':'TEST FIXTURE','listened':True}
                for w in data['words']:w['reviewStatus']='approved'
                core.write(dest/'word-timings.json',data);core.export(fixture_id)
                self.assertEqual(core.verify_current(fixture_id,True)[0]['review']['reviewer'],'TEST FIXTURE')
                (dest/'captions.json').write_text('[]')
                with self.assertRaisesRegex(ValueError,'STALE captions'):core.verify_current(fixture_id,True)
                shutil.copy2(source/'captions.json',dest/'captions.json')
                (dest/'narration.wav').write_bytes(b'changed WAV')
                with self.assertRaisesRegex(ValueError,'STALE'):core.verify_current(fixture_id)
                (dest/'narration.wav').unlink()
                with self.assertRaises(FileNotFoundError):core.verify_current(fixture_id)

    def test_review_requires_listening_and_rejects_stale_or_overlap(self):
        with tempfile.TemporaryDirectory() as directory:
            dest=Path(directory);data=self.sample();core.write(dest/'word-timings.json',data)
            payload={'words':[{k:w[k] for k in ['id','startMs','endMs']} for w in data['words']],'reviewer':'TEST FIXTURE','listened':False,'approve':True,'expectedAlignmentHash':core.sha((dest/'word-timings.json').read_bytes())}
            with patch.object(review,'editable_current',return_value=copy.deepcopy(data)),patch.object(review,'paths',return_value=(dest/'spec.json',dest)),patch.object(review,'export'):
                with self.assertRaisesRegex(ValueError,'Listening'):review.apply_review('fixture',payload)
                bad=copy.deepcopy(payload);bad['expectedAlignmentHash']='stale'
                with self.assertRaisesRegex(ValueError,'Stale'):review.apply_review('fixture',bad)
                bad=copy.deepcopy(payload);bad['words'][1]['startMs']=300
                with self.assertRaisesRegex(ValueError,'overlap'):review.apply_review('fixture',bad)
                payload['approve']=False;payload['words'][0]['startMs']=180
                result=review.apply_review('fixture',payload);self.assertEqual(result['status'],'needs_review')
                self.assertEqual(core.read(dest/'word-timings.json')['words'][0]['corrections'][0]['before'],200)

    def test_corrected_detector_gap_requires_explicit_listened_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            dest=Path(directory);data=self.sample()
            data['unexplainedSpeechGaps']=[{'startMs':700,'endMs':1100,'reviewed':False}]
            core.write(dest/'word-timings.json',data)
            payload={'words':[{k:w[k] for k in ['id','startMs','endMs']} for w in data['words']],'reviewer':'TEST FIXTURE','listened':True,'approve':True,'expectedAlignmentHash':core.sha((dest/'word-timings.json').read_bytes())}
            with patch.object(review,'editable_current',return_value=copy.deepcopy(data)),patch.object(review,'paths',return_value=(dest/'spec.json',dest)),patch.object(review,'export'):
                review.apply_review('fixture',payload)
            gap=core.read(dest/'word-timings.json')['unexplainedSpeechGaps'][0]
            self.assertTrue(gap['reviewed']);self.assertEqual(gap['reviewer'],'TEST FIXTURE')
            # A real speech-energy hole must still block approval, regardless of the checkbox.
            data['words'][1]['startMs']=1100;data['energy20ms']=[.1]*90
            payload['words'][1]['startMs']=1100;payload['expectedAlignmentHash']=core.sha((dest/'word-timings.json').read_bytes())
            with patch.object(review,'editable_current',return_value=data),patch.object(review,'paths',return_value=(dest/'spec.json',dest)),patch.object(review,'export'):
                with self.assertRaisesRegex(ValueError,'speech gap'):review.apply_review('fixture',payload)

if __name__=='__main__':unittest.main()
