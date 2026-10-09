import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import {mkdirSync, writeFileSync} from 'node:fs';
import path from 'node:path';
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const composition = await selectComposition({serveUrl, id: 'StyleProofDebug'});
const reports: unknown[] = [];
let failed = false;
mkdirSync('renders/qa', {recursive: true});
for (const frame of [0, 24, 108, 144, 228, 270, 360, 429]) {
  let received = false;
  await renderStill({serveUrl, composition, frame, output: `renders/qa/layout-${frame}.png`, logLevel: 'error',
    onBrowserLog: log => {
      const index = log.text.indexOf('LAYOUT_AUDIT:');
      if (index < 0) return;
      const report = JSON.parse(log.text.slice(index + 'LAYOUT_AUDIT:'.length));
      reports.push(report); received = true;
      if (report.violations.length || report.collisions.length || report.fonts.some((f: {loaded: boolean}) => !f.loaded)) failed = true;
    }});
  if (!received) throw new Error(`No layout report for frame ${frame}`);
}
writeFileSync('renders/qa/layout-report.json', JSON.stringify(reports, null, 2)+'\n');
if (failed) throw new Error('Layout/font audit failed: inspect renders/qa/layout-report.json');
console.log('Eight real Chromium layouts: fonts, safe area, text overflow and label collisions passed.');
