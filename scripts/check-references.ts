import {execFileSync} from 'node:child_process';
import {readFileSync, writeFileSync, mkdirSync} from 'node:fs';
import {PNG} from 'pngjs';
// Fixed tolerances: accommodate minor rasterization differences, not layout drift.
const MAX_MEAN_ERROR = 0.35;
const MAX_CHANGED_PIXEL_RATIO = 0.002;
mkdirSync('renders/qa', {recursive: true});
execFileSync(process.execPath, ['--import', 'tsx', 'scripts/render.ts', 'refs'], {stdio: 'inherit'});
let failed = false;
const reports = [];
for (const name of ['opening', 'hundred', 'result', 'outro', 'board']) {
  const a = PNG.sync.read(readFileSync(`tests/references/${name}.png`));
  const b = PNG.sync.read(readFileSync(`renders/reference-current/${name}.png`));
  if (a.width !== b.width || a.height !== b.height) throw new Error('Reference dimensions differ');
  const diff = new PNG({width: a.width, height: a.height});
  let total = 0, changed = 0;
  for (let i = 0; i < a.data.length; i += 4) {
    let pixel = 0;
    for (let c = 0; c < 3; c++) {const d = Math.abs(a.data[i+c] - b.data[i+c]); total += d; pixel = Math.max(pixel, d); diff.data[i+c] = d;}
    diff.data[i+3] = 255;
    if (pixel > 8) changed++;
  }
  const meanError = total / (a.width * a.height * 3), changedRatio = changed / (a.width*a.height);
  const pass = meanError <= MAX_MEAN_ERROR && changedRatio <= MAX_CHANGED_PIXEL_RATIO;
  reports.push({name, meanError, changedRatio, pass}); failed ||= !pass;
  if (!pass) writeFileSync(`renders/qa/diff-${name}.png`, PNG.sync.write(diff));
}
writeFileSync('renders/qa/reference-report.json', JSON.stringify({MAX_MEAN_ERROR, MAX_CHANGED_PIXEL_RATIO, reports}, null, 2)+'\n');
console.log(reports);
if (failed) throw new Error('Reference comparison failed. Do not overwrite references or relax tolerances.');
