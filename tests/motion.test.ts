import {test} from 'node:test';
import assert from 'node:assert/strict';
import {ribbonCell} from '../src/episodes/seconds-film/TimeRibbon';
import {cameraBetween} from '../src/components/CameraRig';
import {days, years, blockCount, filmEvents} from '../src/episodes/seconds-film/model';
import study from '../public/episodes/motion-study/narration-manifest.json';
import {validateEpisode, type Episode} from '../src/episodes/types';
test('seconds count and unit conversions are exact before display rounding',()=>{
  assert.equal(blockCount,1000);assert.equal(Math.round(days*10)/10,11.6);assert.equal(Math.round(years*10)/10,31.7);
});
test('camera endpoints and monotone scale preserve geometry',()=>{
  const a={x:10,y:10,scale:24},b={x:300,y:480,scale:.76};
  assert.deepEqual(cameraBetween(-1,0,72,a,b),a);
  assert.ok(Math.abs(cameraBetween(72,0,72,a,b).scale-b.scale)<1e-12);
  let previous=24;
  for(let f=0;f<=72;f++){const c=cameraBetween(f,0,72,a,b);assert.ok(c.scale<=previous+1e-12 && c.scale>=.76-1e-12);previous=c.scale;}
});
test('short-study keeps its own contract and publication review gate',()=>{
  const episode=study as Episode;assert.doesNotThrow(()=>validateEpisode(episode));
  assert.throws(()=>validateEpisode({...episode,durationInFrames:451}),/12–15s/);
  assert.throws(()=>validateEpisode(episode,{publication:true}),/reviewed/);
  const e=filmEvents(episode);assert.equal(e.zoom,episode.captions[2].from);assert.equal(e.years,episode.captions[3].from);
});

test('folded year ribbon preserves all time through row boundaries',()=>{
  let length=0,wrapped=0;
  for(let i=0;i<1000;i++){const c=ribbonCell(i);length+=c.first+c.second;
    assert.ok(c.first>0 && c.second>=0 && c.x+c.first<=640+1e-9);
    assert.ok(c.row>=0 && c.row<4);if(c.second>0) wrapped++;
  }
  assert.ok(Math.abs(length-years*80)<1e-8);assert.equal(wrapped,3);
});
