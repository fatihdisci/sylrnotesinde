import type {CaptionCue} from '../components/CaptionTrack';
export type Episode = {
  id: string; title: string; hook: string; brandVersion: '0.1-candidate';
  kind: 'episode' | 'style-proof' | 'motion-study'; durationInFrames: number;
  narration: readonly {id: string; text: string; from: number; durationInFrames: number; path: string}[];
  sources: readonly {title: string; url?: string; note: string; accessed?: string}[];
  scenes: readonly {id: string; from: number; to: number; purpose: string}[];
  audio: {voiceProvider: string; voiceStatus: 'temporary' | 'final' | 'absent'; sfxPath?: string; musicPath?: string};
  subtitlePath: string; captions: readonly CaptionCue[];
  claims?: readonly {id: string; quantity: 'length' | 'area' | 'volume' | 'count' | 'time'; numerator: number; denominator: number; ratio: number; assumptions: string; scale: 'linear' | 'schematic' | 'logarithmic'}[];
  provenance?: {specHash: string; textHash: string; settingsHash: string; ttsModelHash: string; audioHash: string; alignmentHash: string; captionsHash: string; reviewStatus: string; reviewer?: string | null; wordTimingPath: string};
  timeline?: {narrationStartFrame: number; audioFrames: number; resultFromFrame: number; resultHoldFrames: number; outroFromFrame: number; durationInFrames: number};
};
export const validateEpisode = (episode: Episode, {publication = false}: {publication?: boolean} = {}) => {
  const frame = (n: number) => {if (!Number.isSafeInteger(n) || n < 0) throw new Error('Invalid frame');};
  const {durationInFrames: d} = episode; frame(d);
  if (episode.kind === 'episode' && (d < 1200 || d > 1350)) throw new Error('Episode must be40–45s including outro');
  if (episode.kind === 'motion-study' && (d < 360 || d > 450)) throw new Error('MotionStudy must be12–15s including outro');
  if (episode.brandVersion !== '0.1-candidate') throw new Error('Brand version mismatch');
  const content = d - 45;
  let narrationEnd = 0;
  for (const n of episode.narration) {
    frame(n.from); frame(n.durationInFrames);
    if (!n.durationInFrames || n.from < narrationEnd || !n.path.trim() || !n.text.trim()) throw new Error('Invalid or overlapping narration');
    narrationEnd = n.from + n.durationInFrames;
    if (narrationEnd > content) throw new Error('Narration overlaps outro');
  }
  let captionEnd = 0;
  for (const c of episode.captions) {
    frame(c.from); frame(c.to);
    if (c.from < captionEnd || c.to > content || c.to <= c.from || !c.lines.length || c.lines.length > 2 || c.lines.some(l => !l.trim())) throw new Error('Invalid/overlapping caption');
    captionEnd = c.to;
  }
  let end = 0;
  for (const s of episode.scenes) {
    frame(s.from); frame(s.to);
    if (s.from !== end || s.to <= s.from) throw new Error('Scene gap or overlap');
    end = s.to;
  }
  if (end !== content) throw new Error('Scenes must end before the canonical outro');
  for (const c of episode.claims ?? []) {
    if (!c.id?.trim() || !['length','area','volume','count','time'].includes(c.quantity) || !['linear','schematic','logarithmic'].includes(c.scale) || ![c.numerator, c.denominator, c.ratio].every(Number.isFinite) || c.denominator <= 0 || c.numerator < 0 || Math.abs(c.ratio - c.numerator / c.denominator) > Math.max(1, c.ratio) * 1e-9 || !c.assumptions.trim()) throw new Error('Unverifiable numeric claim');
  }
  if (publication && episode.kind !== 'style-proof') {
    const p = episode.provenance;
    if (!episode.narration.length || !episode.captions.length || !episode.sources.length || episode.sources.some(s => !s.title.trim() || !s.note.trim() || !s.accessed?.trim()) || !episode.claims?.length) throw new Error('Publication requires narration, captions, sources and claims');
    if (!p || p.reviewStatus !== 'approved' || !p.reviewer || ![p.specHash, p.textHash, p.settingsHash, p.ttsModelHash, p.audioHash, p.alignmentHash, p.captionsHash].every(h => /^[a-f0-9]{64}$/.test(h))) throw new Error('Publication requires reviewed, versioned audio/captions');
    if (episode.captions.some(c => c.timingSource !== 'forced-alignment' || !c.wordIds?.length)) throw new Error('Missing aligned caption words');
  }
};
