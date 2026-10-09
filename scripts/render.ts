import {bundle} from '@remotion/bundler';
import {ensureBrowser, renderMedia, renderStill, selectComposition} from '@remotion/renderer';
import {mkdirSync, existsSync} from 'node:fs';
import path from 'node:path';

const mode = process.argv[2] ?? 'all';
if (!['all', 'proof', 'outro', 'board', 'refs', 'debug'].includes(mode)) throw new Error(`Unknown render target: ${mode}`);
for (const asset of ['public/fonts/IBMPlexSans-Regular.woff2', 'public/audio/brand/closing.wav', 'public/episodes/style-proof/hook.wav']) {
  if (!existsSync(asset)) throw new Error(`Prepare local asset before render: ${asset}`);
}
mkdirSync('renders', {recursive: true});
await ensureBrowser();
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts'), webpackOverride: c => c});
const options = {serveUrl, logLevel: 'warn' as const};
for (const [id, file, key] of [['StyleProof', 'style-proof.mp4', 'proof'], ['Outro', 'outro.mp4', 'outro']]) {
  if (mode !== 'all' && mode !== key) continue;
  const composition = await selectComposition({...options, id});
  console.log(`Rendering ${id}: ${composition.durationInFrames} frames`);
  let lastPercent = -1;
  await renderMedia({...options, composition, outputLocation: `renders/${file}`, codec: 'h264',
    pixelFormat: 'yuv420p', crf: 17, audioCodec: 'aac', audioBitrate: '192k', concurrency: 4,
    onProgress: ({progress}) => {
      const percent = Math.floor(progress * 10) * 10;
      if (percent > lastPercent) {console.log(`${id} ${percent}%`); lastPercent = percent;}
    }});
}
if (mode === 'all' || mode === 'board') {
  const composition = await selectComposition({...options, id: 'StyleBoard'});
  await renderStill({...options, composition, frame: 0, output: 'renders/style-board.png', imageFormat: 'png'});
}
if (mode === 'debug') {
  const composition = await selectComposition({...options, id: 'StyleProofDebug'});
  await renderStill({...options, composition, frame: 360, output: 'renders/safe-area-debug.png', imageFormat: 'png'});
}
if (mode === 'refs') {
  mkdirSync('renders/reference-current', {recursive: true});
  for (const [id, frame, name] of [['StyleProof', 30, 'opening'], ['StyleProof', 180, 'hundred'],
    ['StyleProof', 360, 'result'], ['Outro', 24, 'outro'], ['StyleBoard', 0, 'board']] as const) {
    const composition = await selectComposition({...options, id});
    await renderStill({...options, composition, frame, output: `renders/reference-current/${name}.png`, imageFormat: 'png'});
  }
}
console.log('Render complete. Local assets only.');
