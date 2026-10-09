import {readFileSync, existsSync} from 'node:fs';
import {resolve, sep} from 'node:path';
import type {Episode} from '../src/episodes/types';

type PreparedNarration = Pick<Episode, 'narration' | 'audio' | 'subtitlePath' | 'captions'> & {
  brandVersion: Episode['brandVersion']; fps: 30; captionReviewRequired: boolean; recommendedTotalFrames: number;
};
/** Build-time only. Imported assets must be prepared and reviewed before rendering. */
export const loadNarration = (id: string): PreparedNarration => {
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(id)) throw new Error('Invalid episode ID');
  const base = resolve('public');
  const file = resolve(base, 'episodes', id, 'narration-manifest.json');
  const data = JSON.parse(readFileSync(file, 'utf8')) as PreparedNarration;
  if (data.brandVersion !== '0.1-candidate' || data.fps !== 30) throw new Error('Narration format mismatch');
  if (data.captionReviewRequired) throw new Error('Review phrase captions and re-export before rendering');
  if (data.recommendedTotalFrames < 1200 || data.recommendedTotalFrames > 1350) throw new Error('Narration exceeds episode duration');
  for (const segment of data.narration) {
    const asset = resolve(base, segment.path);
    if (!asset.startsWith(base + sep) || !existsSync(asset)) throw new Error('Narration WAV missing or outside public');
    if (segment.from + segment.durationInFrames > data.recommendedTotalFrames - 45) throw new Error('Narration overlaps outro');
  }
  return data;
};
