import {test} from 'node:test';
import assert from 'node:assert/strict';
import manifest from '../public/episodes/solar-basketball/narration-manifest.json';
import {scaleModel,metres,positions} from '../src/episodes/solar-basketball/model';
import {cameraPose,anchor} from '../src/episodes/solar-basketball/camera';
import {validateEpisode,type Episode} from '../src/episodes/types';
const episode=manifest as Episode;
test('Solar model uses one physical scale for diameters and distances',()=>{
 assert.equal(scaleModel.sun.diameter,.24);
 assert.ok(Math.abs(scaleModel.earth.diameter*1000-2.2002587)<.0001);
 assert.ok(Math.abs(scaleModel.earth.distance-25.804225959)<.0001);
 assert.ok(Math.abs(scaleModel.moon.distance*100-6.630444)<.0001);
 assert.ok(Math.abs(scaleModel.jupiter.diameter*100-2.4662958)<.0001);
 assert.ok(Math.abs(scaleModel.neptune.distance-778.784)<.001);
 assert.equal(Math.abs(positions.neptune[2]-positions.sun[2]),metres(4_515_000_000));
 assert.equal(positions.moon[0]-positions.earth[0],metres(384_400));
});
test('Natural voice duration and canonical outro validate without a 45 second cap',()=>{
 validateEpisode(episode);
 assert.equal(episode.audio.voiceProvider,'local:antalia-mini');
 assert.equal(episode.durationInFrames,1979);
 assert.equal(episode.timeline!.outroFromFrame,1934);
 assert.equal(episode.durationInFrames-episode.timeline!.outroFromFrame,45);
 assert.equal(episode.captions.flatMap(c=>c.wordIds).length,144);
});
test('Camera is deterministic, finite and still moves through the real metre world',()=>{
 for(let f=0;f<episode.durationInFrames-45;f++){
  const p=cameraPose(f,episode);
  assert.deepEqual(p,cameraPose(f,episode));
  assert.ok([...p.eye,...p.target,p.fov].every(Number.isFinite));
  assert.ok(p.fov>20&&p.fov<70);
 }
 const wide=cameraPose(episode.durationInFrames-46,episode);
 assert.ok(wide.eye[1]>1600);
 const early=cameraPose(anchor(episode,'earth-size'),episode);
 assert.equal(early.target[2],positions.earth[2]);
});

test('Macro pullback keeps Earth centred until street geometry can take over',()=>{
 const start=anchor(episode,'distance-shock'),stop=anchor(episode,'street');
 for(const f of [start,start+10,start+20,start+30]){
  assert.ok(f<stop);
  assert.deepEqual(cameraPose(f,episode).target,positions.earth);
 }
});
