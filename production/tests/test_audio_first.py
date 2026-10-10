import json,sys,tempfile,unittest,shutil
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import core
from storyboard import resolve_storyboard

class AudioFirstTests(unittest.TestCase):
    def test_duration_has_no_padding_or_speed_change(self):
        for seconds in [7,47,65]:
            t=core.spec_timeline({'audioDurationMs':seconds*1000,'words':[{'endMs':seconds*1000-100}]},{'format':'audio-first','resultHoldFrames':30})
            self.assertEqual(t['durationInFrames'],seconds*30+72)
            self.assertEqual(t['audioFrames'],seconds*30)
    def test_storyboard_rejects_changed_anchor_and_tracks_word_corrections(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'storyboard.json'
            p.write_text(json.dumps({'idea':'fixture','events':[{'id':'reveal','at':{'word':0,'text':'milyar'},'information':'','visual':'','camera':'','animation':'','effects':[]}]}))
            data={'words':[{'id':0,'word':'milyar','startMs':250,'endMs':600}],'audioDurationMs':1000,'script':{'phrases':[{'display':['milyar']} ]},'displayMap':[{'spokenWordIds':[0]}]}
            t={'narrationStartFrame':0,'outroFromFrame':60}
            self.assertEqual(resolve_storyboard(p,data,t)['events'][0]['from'],7)
            data['words'][0]['startMs']=300
            self.assertEqual(resolve_storyboard(p,data,t)['events'][0]['from'],9)
            data['words'][0]['word']='milyon'
            with self.assertRaises(ValueError):resolve_storyboard(p,data,t)
    def test_archived_source_and_script_are_required_for_current_bindings(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);spec=root/'production.json';audio=root/'narration.wav';script=root/'script.txt'
            spec.write_text(json.dumps({'audioSource':{'provider':'user'},'phrases':[{'spoken':'Bir milyar.'}]}));audio.write_bytes(b'normalized');script.write_text('Bir milyar.')
            (root/'original.mp3').write_bytes(b'original')
            core.write(root/'external-audio.json',{'schemaVersion':2,'archivePath':'original.mp3','sourceSha256':core.sha(b'original'),'scriptSha256':core.sha(script.read_bytes()),'processing':'fixture'})
            with patch.object(core,'ROOT',root):
                result=core.bindings(spec,audio);self.assertIn('voiceSourceHash',result);self.assertNotIn('ttsModelHash',result)
                script.write_text('Bir milyon.')
                with self.assertRaisesRegex(ValueError,'transcript changed'):core.bindings(spec,audio)
                script.write_text('Bir milyar.');(root/'original.mp3').write_bytes(b'changed')
                with self.assertRaisesRegex(ValueError,'original audio changed'):core.bindings(spec,audio)
    def test_imported_publication_and_storyboard_stem_gates_on_isolated_assets(self):
        source_spec,source_assets=core.paths('seconds-audio-first')
        if not (source_assets/'sfx-stem.wav').exists():self.skipTest('Import voice and build sound first')
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);dest=root/'assets';spec=root/'production.json'
            shutil.copytree(source_assets,dest);shutil.copy2(source_spec,spec)
            board=root/'storyboard.json';shutil.copy2(source_spec.parent/'storyboard.json',board)
            with patch.object(core,'paths',return_value=(spec,dest)):
                with self.assertRaisesRegex(ValueError,'PUBLICATION BLOCKED'):core.verify_current('seconds-audio-first',True)
                # Approval is simulated only in disposable TEST FIXTURE copies.
                data=core.read(dest/'word-timings.json');data['review']={'status':'approved','reviewer':'TEST FIXTURE','listened':True}
                for w in data['words']:w['reviewStatus']='approved'
                core.write(dest/'word-timings.json',data);core.export('seconds-audio-first')
                self.assertEqual(core.verify_current('seconds-audio-first',True)[0]['review']['reviewer'],'TEST FIXTURE')
                original=board.read_bytes();bad=core.read(board);bad['events'][1]['at']['text']='changed';core.write(board,bad)
                with self.assertRaisesRegex(ValueError,'Storyboard word changed'):core.verify_current('seconds-audio-first')
                board.write_bytes(original);(dest/'sfx-stem.wav').write_bytes(b'changed')
                with self.assertRaisesRegex(ValueError,'STALE sound stem'):core.verify_current('seconds-audio-first')

    def test_solar_music_is_versioned_independently_and_human_gate_remains(self):
        source_spec,source_assets=core.paths('solar-basketball')
        if not (source_assets/'ambient-stem.wav').exists():self.skipTest('Generate the local solar score first')
        with tempfile.TemporaryDirectory() as folder:
            dest=Path(folder)/'assets';dest.mkdir()
            for name in ['narration.wav','external-audio.json','script.txt','word-timings.json','narration-manifest.json','captions.json','captions.srt','sound-design.json','sfx-stem.wav','ambient-stem.wav']:
                shutil.copy2(source_assets/name,dest/name)
            spec=Path(folder)/'production.json';shutil.copy2(source_spec,spec)
            shutil.copy2(source_spec.parent/'storyboard.json',spec.parent/'storyboard.json')
            with patch.object(core,'paths',return_value=(spec,dest)):
                core.verify_current('solar-basketball')
                with self.assertRaisesRegex(ValueError,'PUBLICATION BLOCKED'):core.verify_current('solar-basketball',True)
                (dest/'ambient-stem.wav').write_bytes(b'changed score')
                with self.assertRaisesRegex(ValueError,'STALE music stem'):core.verify_current('solar-basketball')

if __name__=='__main__':unittest.main()
