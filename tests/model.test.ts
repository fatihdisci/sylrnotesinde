import {test} from 'node:test';
import assert from 'node:assert/strict';
import {units, proofState} from '../src/episodes/style-proof/model';
import {toScreen} from '../src/components/ScaleStage';
import {formatTR} from '../src/components/NumberDisplay';
import {validateEpisode} from '../src/episodes/types';
import {styleProofEpisode} from '../src/episodes/style-proof/episode';
import {markGeometry, outroSpec, colors} from '../src/brand/tokens';
import {progress} from '../src/brand/motion';

test('exact 10 → 100 → 1000; no clipped counted units on any content frame', () => {
  assert.equal(units.length, 1000);
  assert.equal(new Set(units.map(u => `${u.x},${u.y}`)).size, 1000);
  let previous = 0;
  for (let f = 0; f < 405; f++) {
    const {count, camera} = proofState(f);
    assert.ok(count >= previous, `Monotonic count at ${f}`);
    for (const u of units.slice(0, count)) {
      const a = toScreen(u.x, u.y, camera), b = toScreen(u.x + 9, u.y + 9, camera);
      assert.ok(a.x >= -0.01 && a.y >= -0.01 && b.x <= 864.01 && b.y <= 560.01, `Clipped unit ${u.id} at ${f}`);
    }
    previous = count;
  }
  for (const [f, count] of [[0, 10], [89, 10], [144, 100], [209, 100], [270, 1000], [404, 1000]])
    assert.equal(proofState(f).count, count);
  for (let block = 0; block < 10; block++) assert.equal(units.filter(u => u.block === block).length, 100);
});
test('Turkish number formatting and typography sample', () => {
  assert.equal(formatTR(1000000), '1.000.000');
  assert.equal(formatTR(11.6, 1), '11,6');
});
test('episode structure and narration cannot overrun outro', () => {
  assert.doesNotThrow(() => validateEpisode(styleProofEpisode));
  assert.throws(() => validateEpisode({...styleProofEpisode, kind: 'episode'}));
  assert.throws(() => validateEpisode({...styleProofEpisode, narration: [{...styleProofEpisode.narration[0], from: 390}]}));
  assert.throws(() => validateEpisode({...styleProofEpisode, captions: [{from: 0, to: 10, lines: ['a', 'b', 'c']}]}));
});
test('brand timing, geometric proportions and easing contract', () => {
  assert.deepEqual(markGeometry.lengths, [24, 40, 64]);
  assert.equal(markGeometry.spacing, 10); assert.equal(markGeometry.stroke, 3); assert.equal(markGeometry.marker, 6);
  assert.equal(outroSpec.frames, 45); assert.equal(outroSpec.lineEnd, 12); assert.equal(outroSpec.markerEnd, 24);
  assert.equal(outroSpec.nameEnd, 20); assert.equal(colors.background, '#111615');
  let last = 0;
  for (let f = 0; f <= 60; f++) {const p = progress(f, 0, 60); assert.ok(p >= last && p <= 1); last = p;}
  assert.equal(last, 1);
});
