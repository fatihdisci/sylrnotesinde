import {test} from 'node:test';
import assert from 'node:assert/strict';
import {coil,cellPose,days,years,unitWidth} from '../src/episodes/seconds-audio-first/geometry';
import {project,morphPoints,type SpatialCamera} from '../src/components/SpatialMotion';
import {validateEpisode,type Episode} from '../src/episodes/types';
import audioFirst from '../public/episodes/seconds-audio-first/narration-manifest.json';
test('1000 identical time units retain length during road-to-coil transformation',()=>{
  for(const amount of [0,.25,.5,.75,1]){
    let total=0;
    for(let i=0;i<1000;i++){const cell=cellPose(i,amount);assert.ok([cell.x,cell.y,cell.angle,cell.length].every(Number.isFinite));assert.equal(cell.length,coil.unit);total+=cell.length;}
    assert.ok(Math.abs(total/coil.unit-1000)<1e-9);
  }
  assert.equal(Math.round(days*10),116);assert.equal(Math.round(years*10),317);
  // Equal arc samples differ from their curved arc only by subpixel chord error.
  const lengths=coil.samples.slice(1).map((p,i)=>Math.hypot(p[0]-coil.samples[i][0],p[1]-coil.samples[i][1]));
  assert.ok(Math.max(...lengths)/Math.min(...lengths)<1.001);
});
test('top-down comparison preserves lengths and does not enlarge the lead unit',()=>{
  const cam:SpatialCamera={target:[0,70,0],scale:.91,pitch:0,yaw:0,roll:0,focal:2600};
  const a=project([0,0,0],cam),b=project([coil.unit,0,0],cam);
  assert.ok(Math.abs(Math.hypot(b[0]-a[0],b[1]-a[1])-.91*coil.unit)<1e-10);
  assert.deepEqual(morphPoints([[0,0]],[[10,20]],.5),[[5,10]]);
  assert.throws(()=>morphPoints([],[[1,1]],.5),/matching/);
  for(let i=0;i<1000;i++){
    const pose=cellPose(i,1),cos=Math.cos(pose.angle),sin=Math.sin(pose.angle);
    for(const x of [-pose.length/2,pose.length/2]) for(const y of [-unitWidth/2,unitWidth/2]){
      const screen=project([pose.x+x*cos-y*sin,pose.y+x*sin+y*cos,0],cam);
      assert.ok(screen[0]>=36&&screen[0]<=1000&&screen[1]>=512&&screen[1]<=1327,`Final unit ${i} clipped`);
    }
  }
});
test('audio-led duration follows the recording while approval remains required',()=>{
  const episode=audioFirst as Episode;
  assert.ok(episode.durationInFrames>1350);
  assert.doesNotThrow(()=>validateEpisode(episode));
  assert.throws(()=>validateEpisode(episode,{publication:true}),/reviewed/);
  assert.throws(()=>validateEpisode({...episode,kind:'episode'}),/40–45/);
  assert.equal(episode.durationInFrames-episode.timeline!.outroFromFrame,45);
});
