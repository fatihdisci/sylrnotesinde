"""Original deterministic PCM synthesis. No services, samples, or random seeds."""
from pathlib import Path
import math
import wave
import struct

RATE = 48000
ROOT = Path(__file__).resolve().parents[1]

def pulse(t, frequency, duration, amplitude):
    if not 0 <= t < duration:
        return 0.0
    attack = min(1, t / 0.004)
    tail = min(1, (duration - t) / 0.025)
    envelope = attack * tail * math.exp(-t * 30 / max(1, frequency / 400))
    return amplitude * envelope * (math.sin(2 * math.pi * frequency * t) + 0.25 * math.sin(2 * math.pi * frequency * 2.37 * t))

def thud(t):
    if not 0 <= t < 0.42:
        return 0.0
    env = min(1, t / 0.012) * min(1, (0.42 - t) / 0.09) * math.exp(-t * 11)
    return 0.25 * env * (math.sin(2 * math.pi * (110 * t - 26 * t * t)) + 0.18 * math.sin(2 * math.pi * 238 * t))

def save(relative, seconds, sample):
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    values = [sample(i / RATE) for i in range(round(seconds * RATE))]
    assert max(map(abs, values)) < 0.9, 'Headroom violation'
    with wave.open(str(path), 'wb') as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(RATE)
        f.writeframes(b''.join(struct.pack('<hh', round(v * 32767), round(v * 32767)) for v in values))
    print(f'{relative}: {seconds}s, peak {20 * math.log10(max(map(abs, values))):.1f} dBFS')

# Two light mechanical contacts, then one short soft low impact.
save('public/audio/brand/closing.wav', 1.5,
     lambda t: pulse(t - 2 / 30, 1460, 0.10, 0.13) + pulse(t - 10 / 30, 1820, 0.09, 0.11) + thud(t - 22 / 30))
# Only measurement lock events: initial row, 100-square lock, 1000-square lock.
save('public/episodes/style-proof/measurements.wav', 13.5,
     lambda t: sum(pulse(t - onset, pitch, 0.18, 0.10) for onset, pitch in [(0.4, 740), (4.8, 590), (9.0, 470)]))
