import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from align import viterbi
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'production'))
from qa import correlate
class AlignmentTests(unittest.TestCase):
    def test_repeated_characters_require_blank(self):
        p=np.full((7,3),.001)
        for i,token in enumerate([0,1,1,0,1,0,0]):p[i,token]=.998
        path,states=viterbi(np.log(p),[1,1],0)
        self.assertEqual(set(path[path%2==1]),{1,3})
        self.assertGreater(np.where(path==3)[0][0],np.where(path==1)[0][-1])
    def test_impossible_missing_tokens_are_rejected(self):
        with self.assertRaises(ValueError):viterbi(np.log(np.array([[.9,.1],[.9,.1]])),[1,1,1],0)
    def test_encoded_sync_detects_real_shift(self):
        rng=np.random.default_rng(42);source=rng.normal(size=48000).astype('float32')
        target=np.zeros(70000,dtype='float32');target[7000:55000]=source*.8
        lag,corr=correlate(source,target,5000)
        self.assertAlmostEqual(lag,2000/48);self.assertGreater(corr,.999)
        self.assertGreater(abs(lag),1000/30)
if __name__=='__main__':unittest.main()
