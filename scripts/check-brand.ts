import {createHash} from 'node:crypto';
import {readFileSync, readdirSync, statSync} from 'node:fs';
const walk = (dir: string): string[] => readdirSync(dir).flatMap(name => {
  const p = `${dir}/${name}`; return statSync(p).isDirectory() ? walk(p) : [p];
});
const protectedFiles = [...walk('src/brand'), ...walk('public/fonts'), ...walk('public/audio/brand'),
  'src/components/EpisodeComposition.tsx', 'scripts/generate-sound.py'].sort();
const manifest = JSON.parse(readFileSync('tests/references/brand-manifest.json', 'utf8')) as {version: string; files: Record<string, string>};
const changed: string[] = [];
for (const p of new Set([...protectedFiles, ...Object.keys(manifest.files)])) {
  let hash = '(missing)';
  try {hash = createHash('sha256').update(readFileSync(p)).digest('hex');} catch { /* Report deletions. */ }
  if (manifest.files[p] !== hash) changed.push(p);
}
if (changed.length) {
  console.error(`Brand changes relative to ${manifest.version}:\n${changed.join('\n')}`);
  console.error('Do not refresh the manifest or reference images to make this pass. Explicit user authorization is required.');
  process.exitCode = 1;
} else console.log(`Brand unchanged: ${protectedFiles.length} protected files, ${manifest.version}.`);
