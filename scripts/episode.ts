import {bundle} from '@remotion/bundler';
import {renderMedia, renderStill, selectComposition, type OpenGlRenderer} from '@remotion/renderer';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {existsSync, mkdirSync, readFileSync, writeFileSync, readdirSync, statSync} from 'node:fs';
import {resolve} from 'node:path';
import {typography} from '../src/brand/tokens';
import {validateEpisode, type Episode} from '../src/episodes/types';

const args = process.argv.slice(2);
const mode = args.shift();
const id = args[args.indexOf('--id') + 1];
const draft = args.includes('--draft');
// Opt in per episode; historical 2D renders retain their renderer settings.
const glArg=args.includes('--gl')?args[args.indexOf('--gl')+1]:undefined;
if(glArg && glArg!=='angle')throw new Error('Supported optional renderer: --gl angle');
const chromiumOptions=glArg?{gl:glArg as OpenGlRenderer}:undefined;
if (!['render', 'qa'].includes(mode ?? '') || !args.includes('--id') || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(id)) throw new Error('Use render|qa --id <id> [--draft]. Default is publication mode.');
execFileSync('python3', ['production/check.py', '--id', id, ...(draft ? [] : ['--release'])], {stdio: 'inherit'});
const episode = JSON.parse(readFileSync(`public/episodes/${id}/narration-manifest.json`, 'utf8')) as Episode;
validateEpisode(episode, {publication: !draft});
execFileSync(process.execPath, ['--import', 'tsx', 'scripts/check-brand.ts'], {stdio: 'inherit'});
const dir = `renders/episodes/${id}`;
mkdirSync(dir, {recursive: true});
const sourceFiles = (dir: string): string[] => readdirSync(dir).sort().flatMap(n => {const p = `${dir}/${n}`; return statSync(p).isDirectory() ? sourceFiles(p) : [p];});
const sourceHash = createHash('sha256'); for (const file of [...sourceFiles('src'),...sourceFiles('public/audio')]) sourceHash.update(file).update(readFileSync(file));
const sceneSourceSha256 = sourceHash.digest('hex');
const videoPath = `${dir}/${draft ? 'draft' : 'final'}.mp4`;
const serveUrl = await bundle({entryPoint: resolve('src/index.ts')});
const composition = await selectComposition({serveUrl,chromiumOptions, id: `Episode-${id}`, inputProps: {episode}});
if (mode === 'render') {
  let lastPercent = -1;
  await renderMedia({serveUrl,chromiumOptions, composition, inputProps: {episode}, outputLocation: videoPath, codec: 'h264', crf: 20, pixelFormat: 'yuv420p', audioCodec: 'aac', audioBitrate: '192k', concurrency: 4,
    onProgress: ({progress}) => {const percent = Math.floor(progress * 5) * 20; if (percent > lastPercent) {console.log(`${percent}%`); lastPercent = percent;}}});
  writeFileSync(`${videoPath}.json`, JSON.stringify({id, draft, sceneSourceSha256, manifestSha256: createHash('sha256').update(readFileSync(`public/episodes/${id}/narration-manifest.json`)).digest('hex'), videoSha256: createHash('sha256').update(readFileSync(videoPath)).digest('hex')}, null, 2));
  console.log(`\n${resolve(videoPath)}`);
} else {
  if (!existsSync(videoPath)) throw new Error('Render this exact mode first.');
  const metadata = JSON.parse(readFileSync(`${videoPath}.json`, 'utf8'));
  if (metadata.sceneSourceSha256 !== sceneSourceSha256 || metadata.manifestSha256 !== createHash('sha256').update(readFileSync(`public/episodes/${id}/narration-manifest.json`)).digest('hex') || metadata.videoSha256 !== createHash('sha256').update(readFileSync(videoPath)).digest('hex')) throw new Error('STALE render: manifest/timings or MP4 changed');
  // Probe every caption midpoint and its boundaries, plus scene transitions.
  const frames = [...new Set([0, episode.durationInFrames - 1, ...episode.captions.flatMap(c => [c.from, Math.floor((c.from + c.to) / 2), c.to - 1]), ...episode.scenes.map(s => s.from), ...(episode.direction?.events.flatMap(e=>[e.from,Math.floor((e.from+e.to)/2),e.to-1])??[])])].sort((a,b) => a-b);
  const review = `${dir}/review`; mkdirSync(review, {recursive: true});
  const layouts: {frame: number; violations: unknown[]; collisions: unknown[]; fonts: {loaded: boolean}[]; rects: {name: string; height: number}[]}[] = [];
  for (const frame of frames) {
    let received = false;
    await renderStill({serveUrl,chromiumOptions, composition: {...composition, props: {episode, debug: true, hideCaptions: false}}, frame, inputProps: {episode, debug: true}, output: `${review}/layout-${frame}.png`, logLevel: 'error', onBrowserLog: log => {
      const pos = log.text.indexOf('LAYOUT_AUDIT:'); if (pos < 0) return;
      layouts.push(JSON.parse(log.text.slice(pos + 13))); received = true;
    }});
    if (!received) throw new Error(`Missing layout report at ${frame}`);
  }
  writeFileSync(`${dir}/layout-qa.json`, JSON.stringify(layouts, null, 2));
  if (layouts.some(l => l.violations.length || l.collisions.length || l.fonts.some(f => !f.loaded) || l.rects.some(r => r.name === 'caption' && r.height > typography.caption * 1.32 * 2 + 1))) throw new Error(`Layout audit failed: ${dir}/layout-qa.json`);
  // Captioned images are extracted from the actual MP4. Uncaptioned controls use the same frame and scene.
  const sampleFrames = [...new Set([episode.captions[0].from + 10, ...[3,6,9,12].map(i => Math.floor((episode.captions[Math.min(i,episode.captions.length-1)].from + episode.captions[Math.min(i,episode.captions.length-1)].to)/2)), episode.captions.at(-1)!.to-1, episode.durationInFrames-20,...(episode.direction?.events.filter((_,i)=>i%3===0).map(e=>Math.floor((e.from+e.to)/2))??[])])];
  for (const frame of sampleFrames) {
    execFileSync('ffmpeg', ['-y','-v','error','-i',videoPath,'-vf',`select=eq(n\\,${frame})`,'-frames:v','1',`${review}/mp4-${frame}.png`]);
    await renderStill({serveUrl,chromiumOptions,composition: {...composition, props: {episode, hideCaptions: true, debug: false}},frame,inputProps:{episode,hideCaptions:true},output:`${review}/no-caption-${frame}.png`,logLevel:'error'});
  }
  execFileSync('alignment/environments/ctc/bin/python', ['production/qa.py','--id',id,'--video',videoPath,...(draft ? [] : ['--release'])], {stdio:'inherit'});
}
