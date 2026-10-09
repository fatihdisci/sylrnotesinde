import {execFileSync} from 'node:child_process';
import {mkdirSync, writeFileSync, unlinkSync} from 'node:fs';
import {narrator} from '../src/episodes/narrator.config';
const dir = 'public/episodes/style-proof';
mkdirSync(dir, {recursive: true});
const phrases = [
  {id: 'hook', text: 'Bir sıfır, ölçeği değiştirir.', from: 4},
  {id: 'hundred', text: 'On sıra, yüz birim.', from: 105},
  {id: 'thousand', text: 'On blok, bin birim.', from: 225},
  {id: 'result', text: 'Her adımda, on katı.', from: 334},
];
const result = phrases.map(p => {
  const aiff = `${dir}/${p.id}.aiff`, path = `${dir}/${p.id}.wav`;
  execFileSync('say', ['-v', narrator.voiceId, '-r', String(narrator.wordsPerMinute), '-o', aiff, p.text]);
  execFileSync('ffmpeg', ['-y', '-i', aiff, '-af', 'loudnorm=I=-19:TP=-3:LRA=7,afade=t=in:d=0.008,areverse,afade=t=in:d=0.035,areverse', '-ar', '48000', '-ac', '1', path], {stdio: 'pipe'});
  const seconds = Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', path], {encoding: 'utf8'}).trim());
  const durationInFrames = Math.ceil(seconds * 30);
  if (p.from + durationInFrames > 405) throw new Error('Voice exceeds content segment');
  unlinkSync(aiff);
  return {...p, path: `episodes/style-proof/${p.id}.wav`, seconds, durationInFrames};
});
writeFileSync(`${dir}/voice-timing.json`, JSON.stringify(result, null, 2) + '\n');
console.log(result);
