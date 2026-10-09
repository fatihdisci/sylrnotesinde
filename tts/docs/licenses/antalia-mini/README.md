---
language:
- tr
license: apache-2.0
library_name: antalia-mini
pipeline_tag: text-to-speech
tags:
- text-to-speech
- tts
- turkish
- flow-matching
- cpu
---

# Antalia-2 Mini

**Türkçe özet.** Antalia-2 Mini, tek sesli, küçük bir Türkçe metinden konuşmaya (TTS) modelidir: toplam
7,6 milyon parametre, 48 kHz çıkış, sıradan bir işlemcide gerçek zamandan çok daha hızlı. Ham metni alır;
sayıları, tarihleri, saatleri, tutarları, kısaltmaları ve metindeki İngilizce ya da marka adlarını kendi
normalleştiricisiyle okunuşa çevirir. Ses sentetik bir erkek sesidir (Antalia-2'nin sesi): gerçek bir
kişinin sesi değildir ve eğitim verisinde gerçek konuşmacı kaydı yoktur. Kod ve model ağırlıkları
Apache-2.0 lisanslıdır. Kurulum: `pip install antalia-mini`. Tarayıcınızda deneyin: https://huggingface.co/spaces/cloud0day3/antalia-mini

---

Antalia-2 Mini (version 1.0.0) is a small Turkish text-to-speech model with one voice. It has 7.62M parameters in total
(acoustic model 3.69M, vocoder 3.93M), produces 48 kHz audio, and runs well faster than real time on a
CPU. It takes raw Turkish text: a text normaliser inside the package turns numbers, dates, times,
amounts, initialisms, web addresses and English or brand words into the way a Turkish speaker says them.

**Try it in your browser:** [huggingface.co/spaces/cloud0day3/antalia-mini](https://huggingface.co/spaces/cloud0day3/antalia-mini)
runs this release entirely on your device with ONNX Runtime Web (no server; the text never leaves the page).

The voice is a synthetic male voice (Antalia-2's voice), not a real person, and the training data
contains no recordings of real speakers. The code and the weights are licensed under Apache-2.0. Its
predecessor, Antalia-1, is at [cloud0day3/antalia-1](https://huggingface.co/cloud0day3/antalia-1).

## Quickstart

```bash
pip install antalia-mini
```

The same wheel is also in this repository (`pip install https://huggingface.co/cloud0day3/antalia-mini/resolve/main/antalia_mini-1.0.0-py3-none-any.whl`).
Python 3.10 or newer; the dependencies are PyTorch, NumPy, safetensors, soundfile and cmudict.

```python
from antalia_mini import Antalia

tts = Antalia()  # downloads the weights (~31 MB) once; uses a CUDA GPU if there is one, else the CPU
speech = tts.say("Randevunuz 14 Ekim Salı günü saat 15:30'da.", path="randevu.wav", seed=0)
print(speech.duration, speech.sample_rate, speech.seed)

# several texts at once (batched on a GPU)
speeches = tts.say(["Merhaba.", "Siparişiniz yola çıktı."], seed=0)

# streaming: the first sentence is synthesised first, then the rest, a few sentences at a time
for chunk in tts.stream(long_text):
    play(chunk)  # float32 numpy array at tts.sample_rate

# telephone or ASR pipelines: 24000, 16000 or 8000 Hz (resampled from 48 kHz)
tts8k = Antalia(sample_rate=8000)

# Apple Silicon: the CPU is the default; the GPU is an option
tts_mps = Antalia(device="mps")
```

Command line: `antalia-mini "Merhaba, size nasıl yardımcı olabilirim?" -o merhaba.wav`.

Options of `say()`: `seed` (the same text, seed and settings give the same audio; without a seed a random
one is drawn and returned in `speech.seed`), `speed` (default 0.95, slightly slower than the voice's own
pace; higher is faster), `steps` (flow-matching steps, default 8; 4 is faster and measurably less
accurate, see Evaluation), `cfg` (classifier-free guidance, default 2.0). `Antalia.normalize(text)` shows the exact text the
model reads. The model runs in fp32; `Antalia(variant="fp16")` downloads the half-size weights file
(converted back to fp32 when loaded; the audio is practically identical).

An output tone is applied by default: a +6 dB low shelf at 210 Hz and a -9 dB high shelf at 4 kHz,
designed for the chosen output rate, followed by a soft peak limiter that keeps the output below full
scale (no per-utterance loudness normalisation). Pass `eq=False` (to `Antalia`, `say` or `stream`, or
`--no-eq` on the command line) for the raw output. `stream()` carries the filter state across chunks, so
the joined chunks are identical to `say()`'s output.

Two reading fixes are on by default. A text that starts with "ö" or "ı" is spoken after a short "ee,"
that is cut out of the audio again, because the voice tends to put a stray "l" in front of those
sounds at the very start (see Limitations); and double sounds, inside a word ("berraktı") or across a
word gap ("alerjim mahvediyor"), are held a little longer, as Turkish speakers do. Both can be turned
off: `Antalia(prefix="", gem_stretch=1.0)`.

## Samples

Raw input text, seed 0, default settings (8 steps, cfg 2.0, output tone).

| | Text | Audio |
|---|---|---|
| Greeting | Merhaba, size nasıl yardımcı olabilirim? | <audio controls src="https://huggingface.co/cloud0day3/antalia-mini/resolve/main/samples/01-greeting.wav"></audio> |
| Date and time | Randevunuz 14 Ekim Salı günü saat 15:30'da, Dr. Ayşe Yılmaz ile. | <audio controls src="https://huggingface.co/cloud0day3/antalia-mini/resolve/main/samples/02-appointment.wav"></audio> |
| Amount | Toplam tutar 1.250,75 TL. Ödemeyi 3 taksitle yapabilirsiniz. | <audio controls src="https://huggingface.co/cloud0day3/antalia-mini/resolve/main/samples/03-amount.wav"></audio> |
| Phone and e-mail | Bize 0212 555 12 34 numarasından veya destek@ornek.com adresinden ulaşabilirsiniz. | <audio controls src="https://huggingface.co/cloud0day3/antalia-mini/resolve/main/samples/04-phone.wav"></audio> |
| Date | Kargonuz yola çıktı; tahmini teslimat tarihi 9 Ekim 2026, Perşembe. | <audio controls src="https://huggingface.co/cloud0day3/antalia-mini/resolve/main/samples/05-cargo.wav"></audio> |
| Question | Siparişinizi iptal etmek mi istiyorsunuz, yoksa teslimat adresini mi değiştirmek istiyorsunuz? | <audio controls src="https://huggingface.co/cloud0day3/antalia-mini/resolve/main/samples/06-question.wav"></audio> |
| Brand word | Toplantı bağlantısını WhatsApp üzerinden ve e-posta ile gönderdik. | <audio controls src="https://huggingface.co/cloud0day3/antalia-mini/resolve/main/samples/07-english.wav"></audio> |
| Long sentence | İstanbul'un iki yakasını birbirine bağlayan köprüler, her gün yüz binlerce kişinin işe, okula ve evine ulaşmasını sağlıyor; ancak yoğun saatlerde trafik, yolculuk süresini kimi zaman iki katına çıkarabiliyor. | <audio controls src="https://huggingface.co/cloud0day3/antalia-mini/resolve/main/samples/08-long.wav"></audio> |

## Evaluation

Freya-TR-Eval ([freyavoice/freya-tr-eval](https://huggingface.co/datasets/freyavoice/freya-tr-eval)), all
495 sentences, raw text in. Protocol, following EMA Lightning's card and Freya's reference scorer:

- intelligibility: each clip is resampled to 8 kHz and back to 16 kHz (band matching), transcribed by
  faster-whisper large-v3 (fp16, beam 5, language tr, other options at their defaults); reference and
  transcript get Freya's Turkish normalisation; WER and CER are computed over the whole set with jiwer;
- naturalness: UTMOS22-strong, mean over clips, on the full band (resampled to 16 kHz) and on the
  8 kHz band (the same band-matched audio the WER uses);
- 3 seeds per system unless noted; WER gives the mean, with the lowest and highest seed in brackets;
- Antalia-2 Mini with its default settings; EMA Lightning reproduced on our harness with the same
  protocol.

| System | Parameters | WER % | CER % | UTMOS | UTMOS (8 kHz band) |
|---|---|---|---|---|---|
| **Antalia-2 Mini 1.0.0** (default, 8 steps) | 7.62M | **0.97** (0.89–1.12) | **0.19** | 3.25 | **3.06** |
| Antalia-2 Mini 1.0.0, 4 steps | 7.62M | 1.17 (1.12–1.20) | 0.23 | 3.24 | 3.06 |
| EMA Lightning 1.0.1 (our run) | 8.6M | 1.00 (0.89–1.17) | 0.20 | 3.30 | 2.88 |
| VoxCPM2 speaking the same voice (the teacher; 1 seed) | much larger | 0.92 | 0.20 | 3.42 | 3.25 |

With its default settings Antalia-2 Mini makes the fewest character errors and is level with EMA
Lightning on word errors. On this harness: CER 0.19% vs 0.20%, WER 0.97% vs 1.00%. In a second,
independent run on the public benchmark page's harness (other seeds, one NVIDIA L4): CER 0.20% vs
0.22%, the lowest of the 15 Turkish systems measured there, and WER 1.05% vs 1.04%. Both models vary
by about ±0.1 WER from seed to seed, so the WER difference is within noise either way. EMA Lightning is ahead on full-band UTMOS (3.30 vs 3.25); Antalia-2 Mini scores higher on UTMOS
in the 8 kHz band, the band a phone call carries, and is smaller (7.62M vs 8.6M parameters). EMA
Lightning's own card reports 0.92 / 0.18 / ~3.30 on the same protocol.

The two reading fixes (see Quickstart) were found by studying where the model went wrong: the first
in its training data, the second in this benchmark's errors. To check that the second one is not
tuned to the benchmark, we compared both settings on 500 other sentences (160 of our own test prompts
and 340 held-out lines of the training corpus, never trained on): WER 6.12% → 6.02%, CER 1.53% →
1.48%, 3 seeds each. (WER is higher there because those lines contain digits, abbreviations and
foreign names that the scoring normalisation does not match.) The teacher row is the system that generated Antalia-2
Mini's training audio, given for reference; it is not a small model. None of the evaluation sentences,
or near-duplicates of them, were in the training text.

### On the public benchmark page

We also keep an independent re-run of Freya-TR-Eval for every Turkish system we could run, at
[speech.patientdesk.ai/benchmarks](https://speech.patientdesk.ai/benchmarks) (scripts and per-clip
transcripts: [PatientdeskAI/freya-tr-eval-rerun](https://huggingface.co/datasets/PatientdeskAI/freya-tr-eval-rerun)).
It uses EMA Lightning's published eval.py for scoring, 3 seeded takes per system, and one NVIDIA L4 for
speed; Antalia-2 Mini ran there with its default settings, separately from the run above (other seeds).
Sorted by WER; best value per column in bold; API systems have no RTF.

| # | System | Parameters | WER % | CER % | Clean sentences | UTMOS | RTF (L4) |
|---|---|---|---|---|---|---|---|
| 1 | EMA Lightning (plain PyTorch) | 8.6M | **1.04** ± 0.17 | 0.22 | **93.7%** | 3.30 | 0.017 |
| 2 | **Antalia-2 Mini** | 7.62M | 1.05 ± 0.07 | **0.20** | 93.1% | 3.25 | 0.043 |
| 3 | Trendyol-TTS (cfg 2.0, 16 steps) | 2.38B | 1.16 ± 0.16 | 0.23 | 93.1% | **3.82** | 0.962 |
| 4 | Gemini 3.8 Flash TTS (voice Kore) | – | 1.23 ± 0.10 | 0.29 | 92.9% | 3.53 | – |
| 5 | Gemini 3.8 Flash-Lite TTS (voice Kore) | – | 1.34 ± 0.19 | 0.27 | 91.9% | 3.63 | – |
| 6 | Anka TTS (built-in male voice) | 336M | 1.42 ± 0.06 | 0.30 | 91.6% | 3.52 | 0.322 |
| 7 | Alania-2 (production API, voice F1) | 488M | 1.44 ± 0.15 | 0.28 | 91.7% | 3.67 | – |
| 8 | Chatterbox Multilingual (Anka male reference) | 500M | 1.91 ± 0.35 | 0.43 | 88.8% | 3.51 | 2.892 |
| 9 | Piper (tr_TR dfki medium, CPU) | 16M | 3.41 ± 0.21 | 0.73 | 79.4% | 3.71 | 0.038 |
| 10 | XTTS-v2 (Anka male reference) | 470M | 3.67 ± 0.37 | 1.50 | 77.1% | 2.97 | 0.455 |
| 11 | Alania-1 (production API) | 3.3B | 5.99 ± 0.47 | 1.81 | 67.3% | 3.19 | – |
| 12 | Antalia-1 (open weights, release recipe) | 305M | 6.28 ± 0.27 | 2.49 | 66.7% | 2.72 | 0.476 |
| 13 | MMS-TTS (tur) | 36M | 6.38 ± 0.19 | 1.48 | 65.7% | 3.79 | 0.014 |
| 14 | Coqui GlowTTS (tr common-voice, lowercased input) | 28M | 10.93 ± 0.00 | 2.96 | 46.1% | 3.08 | 0.015 |
| 15 | FreyaTTS-small (default voice) | 183M | 12.02 ± 0.00 | 4.95 | 47.1% | 2.81 | 0.286 |

Antalia-2 Mini makes the fewest character errors of the 15 systems and is second on word errors, 0.01
points behind EMA Lightning, well within either model's seed-to-seed spread. EMA Lightning is about 2.5
times faster on the L4 at Antalia-2 Mini's default 8 steps. "Clean sentences" is the share of sentences
transcribed without a single word error.

## Size and speed

| | Antalia-2 Mini | EMA Lightning 1.0.1 |
|---|---|---|
| Parameters | 7.62M (acoustic 3.69M + vocoder 3.93M) | 8.6M |
| Weights | 30.5 MB fp32, 15.3 MB fp16 | |
| Output | 48 kHz (24 / 16 / 8 kHz by resampling) | |
| RTF, NVIDIA L40S, batch 1 | 0.026 | 0.0126 (plain PyTorch, same machine) |
| RTF, CPU, 8 cores (AMD EPYC 7R13) | 0.052 | 0.071 (same machine) |
| RTF, Apple M5 CPU, 2 threads | 0.019 | |
| Time to first audio, `stream()`, Apple M5 CPU | 0.06 s | |

RTF is synthesis time divided by audio duration (lower is faster; 0.01 means one second of speech takes
10 ms), default settings (8 steps, cfg 2.0), batch 1 after a warm-up, the first 100 benchmark sentences,
through each package's own API (text normalisation and output processing included). On a GPU, single
requests are about 2 times slower than EMA Lightning's at the default 8 steps; on a CPU, Antalia-2 Mini
is about 1.4 times faster on the same 8 cores. On an Apple M5 laptop it speaks about 50 times faster
than real time on 2 CPU threads. The Apple M5 numbers were measured with other applications running,
so a quiet machine may be a little faster. On Apple Silicon the
package uses 2 CPU threads by default, which measured faster than 4 or more; elsewhere set
`Antalia(threads=N)` to taste.

## Model

| Part | What | Parameters |
|---|---|---|
| Text encoder | character embeddings, 3 ConvNeXt blocks, 1 self-attention block with RoPE (d=192) | 0.83M |
| Duration predictor | 3 convolutions; trained on durations from monotonic alignment search (no external aligner) | 0.17M |
| Mel generator | 5 DiT blocks (d=192, adaLN-single) over pairs of 128-band log-mel frames at 93.75 Hz; flow matching with shortcut self-consistency, so the one model samples in 1, 2, 4 or 8 steps; classifier-free guidance | 2.69M |
| Vocoder | Vocos-style ConvNeXt stack (d=256, 8 blocks) predicting an n_fft 2048 / hop 512 STFT, one inverse STFT to 48 kHz; fine-tuned on the generator's own mels | 3.93M |

The model reads characters, not phonemes: Turkish spelling is close to pronunciation, and the
normaliser handles the cases where it is not. The methods are reimplemented from the papers: monotonic
alignment search (Glow-TTS, Matcha-TTS), flow matching (Lipman et al., 2023), shortcut models (Frans et
al., 2024), adaLN-single (PixArt-α), ConvNeXt, Vocos, HiFi-GAN and UnivNet discriminators (training only).

## Voice

One voice: a synthetic male voice (Antalia-2's voice), not a real person. The model has no speaker
input and cannot clone voices.

## Training data

About 1,578 hours of synthetic speech, all in Antalia-2's voice, generated with
[VoxCPM2](https://huggingface.co/openbmb/VoxCPM2) (OpenBMB, Apache-2.0) from a reference of that voice. No
recordings of real speakers were used. The text came from:

- Turkish Wikipedia (CC BY-SA 4.0) and FineWeb-2 Turkish (ODC-By 1.0);
- customer-service style sentences (appointments, banking, retail, deliveries) written with a
  language model (Qwen3);
- templates for numbers, dates, times, amounts, phone numbers and codes;
- all of it passed through the same normaliser the package uses, and sentences overlapping
  Freya-TR-Eval removed.

Every generated clip was checked automatically (Whisper large-v3 transcript against the text, UTMOS,
and similarity to the voice) and dropped if it failed.

## Text normaliser

The normaliser is PatientDesk AI's Turkish serving normaliser, released here under the same licence.
It spells out cardinal and ordinal numbers, decimals, percentages, dates, times, ranges, amounts in
lira and other currencies, phone numbers, e-mail and web addresses and common abbreviations, reads
initialisms with Turkish letter names, and respells English and brand words the way they are said in
Turkish (using the CMU Pronouncing Dictionary and a reviewed brand lexicon). `Antalia.normalize(text)`
shows its output.

## Limitations

- One voice, one speaking style; no emotion or style control beyond speed.
- Turkish only. English words inside Turkish sentences are respelled; whole English sentences are not
  supported.
- Short interjections on their own ("Evet.", "Hı hı.", "Tamam!") are its weakest area: they can come out
  flat or rushed. In running text they are packed together with neighbouring sentences, which helps.
- Readings follow the normaliser. Roman numerals ("XIX. yüzyıl"), ordinals written before names
  ("2. Abdülhamit"), unusual formats, rare abbreviations and some foreign names can be read wrongly;
  check `Antalia.normalize(text)` when a reading matters.
- Long inputs are split into sentence-sized chunks (up to about 18 seconds each) and joined with short
  pauses; prosody does not carry across chunks.
- At the very start of a text the voice tends to put a stray "l" before "ö" (and, less often, a "d" or
  "b" before "ı"): the model learned it from its training audio. The default "ee," trick hides it at the
  start of each chunk; a fix in the training data is planned.
- The numbers above are automatic metrics on one benchmark, not listening tests.

## Responsible use

- Tell listeners when they are hearing a synthetic voice.
- Do not use the model to impersonate real people or to make speech that could be mistaken for a
  real person's statement.
- Do not use it for fraud, harassment, or deceptive calls.

## License

The code, the text normaliser and the model weights are all licensed under Apache-2.0 (see LICENSE and
NOTICE in this repository). The `cmudict` dependency is BSD-licensed.

## Credits

- [VoxCPM2](https://huggingface.co/openbmb/VoxCPM2) by OpenBMB, which generated the training audio.
- [Freya-TR-Eval](https://huggingface.co/datasets/freyavoice/freya-tr-eval) and Freya's reference scorer,
  for the benchmark.
- [EMA Lightning](https://pypi.org/project/ema-lightning/), the Turkish model we compare against.
- The CMU Pronouncing Dictionary, through the `cmudict` package.
- Turkish Wikipedia and FineWeb-2 for the training text.

## Citation

```bibtex
@misc{antalia_mini_2026,
  title        = {Antalia-2 Mini: a small Turkish text-to-speech model},
  version      = {1.0.0},
  author       = {{PatientDesk AI}},
  year         = {2026},
  howpublished = {\url{https://huggingface.co/cloud0day3/antalia-mini}}
}
```
