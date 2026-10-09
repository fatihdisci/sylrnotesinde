import type {CaptionCue} from '../components/CaptionTrack';
export type Episode = {
  id: string; title: string; hook: string; brandVersion: '0.1-candidate';
  kind: 'episode' | 'style-proof'; durationInFrames: number;
  narration: readonly {id: string; text: string; from: number; durationInFrames: number; path: string}[];
  sources: readonly {title: string; url?: string; note: string; accessed?: string}[];
  scenes: readonly {id: string; from: number; to: number; purpose: string}[];
  audio: {voiceProvider: string; voiceStatus: 'temporary' | 'final' | 'absent'; sfxPath?: string; musicPath?: string};
  subtitlePath: string; captions: readonly CaptionCue[];
};
export const validateEpisode = (episode: Episode) => {
  const {durationInFrames: d} = episode;
  if (episode.kind === 'episode' && (d < 1200 || d > 1350)) throw new Error('Episode must be 40–45 s including outro');
  if (episode.brandVersion !== '0.1-candidate') throw new Error('Brand version mismatch');
  for (const n of episode.narration) if (n.from + n.durationInFrames > d - 45) throw new Error('Narration overlaps outro');
  for (const c of episode.captions) if (c.lines.length > 2 || c.to > d - 45 || c.to <= c.from) throw new Error('Invalid caption');
  let end = 0;
  for (const s of episode.scenes) {
    if (s.from !== end || s.to <= s.from) throw new Error('Scene gap or overlap');
    end = s.to;
  }
  if (end !== d - 45) throw new Error('Scenes must end before the canonical outro');
};
