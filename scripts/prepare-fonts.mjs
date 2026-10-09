import {copyFile, mkdir, writeFile} from 'node:fs/promises';
await mkdir('public/fonts', {recursive: true});
for (const [pkg, family, weights] of [
  ['plex-sans', 'IBMPlexSans', ['Regular', 'Medium', 'SemiBold']],
  ['plex-mono', 'IBMPlexMono', ['Regular', 'Medium']],
]) {
  for (const weight of weights) {
    const name = `${family}-${weight}.woff2`;
    await copyFile(`node_modules/@ibm/${pkg}/fonts/complete/woff2/${name}`, `public/fonts/${name}`);
  }
  await copyFile(`node_modules/@ibm/${pkg}/fonts/complete/woff2/license.txt`, `public/fonts/LICENSE-${family}.txt`);
}
await writeFile('public/fonts/SOURCE.md', `# Local IBM Plex assets\n\nOfficial publisher: IBM, https://github.com/IBM/plex\nPackages: @ibm/plex-sans 1.1.0; @ibm/plex-mono 2.5.0 (exact versions in lockfile).\nComplete WOFF2 files, not Latin-only subsets. Downloaded 2026-10-09 from the official IBM npm packages.\nSIL Open Font License 1.1: see adjacent LICENSE files.\nUse npm run assets:fonts only to restore these exact assets; never during rendering.\n`);
