import voice from '../../../public/episodes/style-proof/voice-timing.json';
import type {Episode} from '../types';
export const styleProofEpisode = {
  id: 'style-proof', title: 'Bir sıfır, ölçeği değiştirir.', hook: 'Bir sıfır, ölçeği değiştirir.',
  brandVersion: '0.1-candidate', kind: 'style-proof', durationInFrames: 450,
  narration: voice,
  sources: [{title: 'Onluk sistem — doğrudan sayım', note: '10 × 10 = 100; 10 × 100 = 1.000. Her kare tam bir birimdir. Sayılar model testleriyle doğrulanır; dış bilimsel iddia yok.'}],
  scenes: [
    {id: 'ten', from: 0, to: 90, purpose: 'On birimlik sıra, somut açılış'},
    {id: 'hundred', from: 90, to: 210, purpose: 'Kamera geri çekilir; on sıra ortaya çıkar'},
    {id: 'thousand', from: 210, to: 330, purpose: 'Kamera on adet yüzlük bloğu ortaya çıkarır'},
    {id: 'hold', from: 330, to: 405, purpose: 'Ölçüm ilişkisi sabit tutulur'},
  ],
  audio: {voiceProvider: 'macos-say/Yelda', voiceStatus: 'temporary', sfxPath: 'episodes/style-proof/measurements.wav'},
  subtitlePath: 'episodes/style-proof/captions.srt',
  captions: [
    {from: 0, to: 90, lines: ['10 kare. Her biri bir birim.']},
    {from: 90, to: 210, lines: ['10 sıra × 10 birim = 100']},
    {from: 210, to: 330, lines: ['10 blok × 100 birim = 1.000']},
    {from: 330, to: 405, lines: ['Her adımda, 10 katı.', '10 → 100 → 1.000']},
  ],
} as const satisfies Episode;
