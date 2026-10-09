import {bundle} from '@remotion/bundler';
import {ensureBrowser, renderMedia, renderStill, selectComposition} from '@remotion/renderer';
import {existsSync, mkdirSync, readFileSync} from 'node:fs';
import path from 'node:path';
import type {VoiceReelProps} from '../src/compositions/VoiceComparisonReel';
const inputProps = JSON.parse(readFileSync('tts/comparison/reel-manifest.json', 'utf8')) as VoiceReelProps;
if (inputProps.clips.length !== 12 || new Set(inputProps.clips.map(c => `${c.model}|${c.voice}`)).size !== 12) throw new Error('Exactly twelve distinct real profiles required');
let end = 0;
for (const clip of inputProps.clips) {
  if (clip.fromFrame !== end || !existsSync(path.join('public', clip.audio))) throw new Error('Missing or non-contiguous prepared audio');
  end += clip.durationInFrames;
}
if (inputProps.durationInFrames !== end + 45) throw new Error('Canonical outro timing mismatch');
mkdirSync('renders/voice-comparison-review', {recursive: true});
await ensureBrowser();
const serveUrl = await bundle({entryPoint: path.resolve('src/voice-comparison.tsx')});
const options = {serveUrl, inputProps, logLevel: 'warn' as const};
const composition = await selectComposition({...options, id: 'VoiceComparisonReel'});
let previous = -1;
await renderMedia({...options, composition, outputLocation: 'renders/tts-12-profiles.mp4', codec: 'h264',
  pixelFormat: 'yuv420p', crf: 23, audioCodec: 'aac', audioBitrate: '192k', concurrency: 4,
  onProgress: ({progress}) => {const percent = Math.floor(progress * 10) * 10; if (percent > previous) {console.log(`${percent}%`); previous = percent;}}});
for (const index of [0, 1, 2, 6, 7, 11]) {
  await renderStill({...options, composition, frame: inputProps.clips[index].fromFrame + 30,
    output: `renders/voice-comparison-review/profile-${index + 1}.png`});
}
console.log('Rendered twelve-profile comparison, local audio only.');
