"""Model-specific inference. Paths are mandatory local assets, never remote IDs."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]

class AntaliaAdapter:
    def __init__(self, device='cpu'):
        from antalia_mini import Antalia
        self.engine = Antalia(ROOT/'models/antalia-mini', device=device, threads=2, warmup=False)
    def generate(self, text, voice, speed, seed):
        from antalia_mini.api import model_text
        speech = self.engine.say(text, speed=.95*speed, seed=seed)
        return speech.audio, speech.sample_rate, [], model_text(text)

class EMAAdapter:
    def __init__(self, device='cpu'):
        import torch
        from ema_lightning import EMA
        from ema_lightning.model import load_acoustic
        from ema_lightning.decoder import load_decoder
        from ema_lightning.frontend import Frontend
        torch.set_num_threads(2)
        path = ROOT/'models/ema-lightning'
        model = load_acoustic(path/'ema.pt', device)
        decoder = load_decoder(path/'decoder.pt', device)
        self.engine = EMA._from_parts(model, decoder, Frontend(model.vocab), device)
        self.engine._batch_size = 1
    def generate(self, text, voice, speed, seed):
        from dataclasses import asdict
        speech = self.engine.say(text, speed=speed, seed=seed)
        return speech.audio, speech.sample_rate, [asdict(w) for w in speech.words], None

class SupertonicAdapter:
    def __init__(self, device='cpu'):
        if device != 'cpu': raise ValueError('Pinned official ONNX implementation supports CPU; no MPS implementation.')
        import onnxruntime as ort
        from adapters import supertonic_helper as helper
        self.helper = helper
        path = str(ROOT/'models/supertonic-3/onnx')
        opts = ort.SessionOptions()
        opts.intra_op_num_threads = 2
        opts.inter_op_num_threads = 1
        self.engine = helper.TextToSpeech(helper.load_cfgs(path), helper.load_text_processor(path), *helper.load_onnx_all(path, opts, ['CPUExecutionProvider']))
    def generate(self, text, voice, speed, seed):
        import numpy as np
        np.random.seed(seed)
        style = self.helper.load_voice_style([str(ROOT/f'models/supertonic-3/voice_styles/{voice}.json')])
        pieces=[]
        for chunk in self.helper.chunk_text(text):
            wav, duration = self.engine._infer([chunk], ['tr'], style, total_step=8, speed=1.05*speed)
            # Trim each ONNX padded chunk separately; never truncate the final spoken sentence.
            if pieces: pieces.append(np.zeros(round(.3*self.engine.sample_rate), dtype=np.float32))
            pieces.append(wav.reshape(-1)[:int(float(duration[0])*self.engine.sample_rate)])
        return np.concatenate(pieces), self.engine.sample_rate, [], None

ADAPTERS = {'antalia-mini': AntaliaAdapter, 'ema-lightning': EMAAdapter, 'supertonic-3': SupertonicAdapter}
