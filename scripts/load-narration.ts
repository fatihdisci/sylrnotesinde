import {readFileSync, existsSync} from 'node:fs';
import {resolve, sep} from 'node:path';
import {execFileSync} from 'node:child_process';
import {validateEpisode, type Episode} from '../src/episodes/types';
/** Build-time only. Draft preview is explicit; publication validates real asset hashes. */
export const loadNarration = (id: string, {publication = true}: {publication?: boolean} = {}): Episode => {
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(id)) throw new Error('Invalid episode ID');
  const base = resolve('public');
  const data = JSON.parse(readFileSync(resolve(base, 'episodes', id, 'narration-manifest.json'), 'utf8')) as Episode;
  for (const segment of data.narration) {
    const asset = resolve(base, segment.path);
    if (!asset.startsWith(base + sep) || !existsSync(asset)) throw new Error('Narration WAV missing or outside public');
  }
  if (!data.provenance) throw new Error('Legacy audio-only manifest: prepare forced alignment before production');
  execFileSync('python3', ['production/check.py', '--id', id, ...(publication ? ['--release'] : [])]);
  validateEpisode(data, {publication});
  return data;
};
