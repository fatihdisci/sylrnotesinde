import {test} from 'node:test';
import assert from 'node:assert/strict';
import {validateEpisode, type Episode} from '../src/episodes/types';
import fixture from '../public/episodes/production-check/narration-manifest.json';
const episode = fixture as Episode;
test('draft accepts real aligned M1, publication blocks unreviewed captions', () => {
  assert.doesNotThrow(() => validateEpisode(episode));
  assert.throws(() => validateEpisode(episode, {publication: true}), /reviewed/);
});
test('reject negative, fractional, NaN, overlapping and outro-crossing frames', () => {
  for (const from of [-1, 1.5, NaN, Infinity]) assert.throws(() => validateEpisode({...episode, narration: [{...episode.narration[0], from}]}));
  assert.throws(() => validateEpisode({...episode, narration: [...episode.narration, {...episode.narration[0], id: 'duplicate'}]}));
  for (const captions of [[{from: -1, to: 10, lines: ['Ölçek']}], [{from: 0, to: 50, lines: ['a']}, {from: 49, to: 60, lines: ['b']}], [{from: 100, to: 1200, lines: ['a']}], [{from: 0, to: 10.5, lines: ['a']}], [{from: 0, to: 10, lines: ['']}]] ) assert.throws(() => validateEpisode({...episode, captions}));
});
test('publication rejects missing captions, assets, provenance and incorrect claims', () => {
  assert.throws(() => validateEpisode({...episode, captions: []}, {publication: true}));
  assert.throws(() => validateEpisode({...episode, narration: [{...episode.narration[0], path: ''}]}));
  assert.throws(() => validateEpisode({...episode, provenance: undefined}, {publication: true}));
  assert.throws(() => validateEpisode({...episode, claims: [{...episode.claims![0], ratio: 100}]}));
});
