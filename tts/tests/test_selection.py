import sys, unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import selection

class NarratorSelectionTests(unittest.TestCase):
    def test_default_setup_uses_only_user_selected_model(self):
        self.assertEqual(list(selection.selected_models()),['supertonic-3'])
        config=selection.narrator_config()
        self.assertEqual(config['settings'][config['activeModel']],{'voice':'M1','speed':1.0})
        self.assertEqual(config['device'],'cpu')
    def test_explicit_candidate_and_comparison_are_available(self):
        self.assertEqual(list(selection.selected_models('ema-lightning')),['ema-lightning'])
        self.assertEqual(len(selection.selected_models(all_models=True)),3)
    def test_unselected_comparison_bootstrap(self):
        with patch.object(selection,'narrator_config',return_value={'activeModel':None}):
            self.assertEqual(len(selection.selected_models()),3)
