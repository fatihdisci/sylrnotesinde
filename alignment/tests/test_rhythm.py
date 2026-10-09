import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'production'))
from rhythm import inspect_rhythm
class RhythmTests(unittest.TestCase):
    def test_silent_still_pause_is_reviewed_not_failed(self):
        rgb=np.zeros((100,192,108,3),dtype=np.uint8);audio=np.zeros(160000)
        r=inspect_rhythm(rgb,audio,annotations=[{'from':0,'to':100,'purpose':'Read result'}])
        self.assertFalse(r['automaticFailure'])
        self.assertEqual(len(r['silentAndNearlyStaticIntervals']),1)
        self.assertEqual(r['silentAndNearlyStaticIntervals'][0]['authorNotes'],['Read result'])
    def test_short_or_audible_pause_is_not_combined(self):
        rgb=np.zeros((50,192,108,3),dtype=np.uint8)
        self.assertFalse(inspect_rhythm(rgb,np.zeros(80000))['silentAndNearlyStaticIntervals'])
        rgb=np.zeros((100,192,108,3),dtype=np.uint8)
        self.assertFalse(inspect_rhythm(rgb,np.full(160000,.1))['silentAndNearlyStaticIntervals'])
