import {test} from 'node:test';
import assert from 'node:assert/strict';
import {PerspectiveCamera,Vector3} from 'three';
import m from '../public/episodes/seconds-sculpture/narration-manifest.json';
import type {Episode} from '../src/episodes/types';
import {anchor,blockPose,cameraPose,lattice} from '../src/episodes/seconds-sculpture/choreography';
const e=m as Episode;
test('time sculpture retains1000 distinct equal solids through camera reveal and extraction',()=>{
 assert.equal(new Set(Array.from({length:1000},(_,i)=>lattice(i).join(','))).size,1000);
 for(let f=anchor(e,'launch');f<e.durationInFrames-45;f+=7){
  for(let i=0;i<1000;i++){const p=blockPose(i,f,e);assert.equal(p.scale,1);assert.ok([...p.position,...p.rotation].every(Number.isFinite));}
 }
 const from=blockPose(999,anchor(e,'launch'),e);assert.ok(from.position.every(v=>Math.abs(v)<1e-9));
});
test('the complete final sculpture and extracted source stay above captions inside the1080 master',()=>{
 for(let f=anchor(e,'compare')+60;f<e.durationInFrames-45;f+=3){
  const p=cameraPose(f,e),camera=new PerspectiveCamera(p.fov,1080/1920,.08,250);camera.position.set(...p.eye);camera.lookAt(...p.target);camera.updateMatrixWorld();
  for(let i=0;i<1000;i++)for(const x of [-.5,.5])for(const y of [-.5,.5])for(const z of [-.5,.5]){
   const pos=blockPose(i,f,e).position;const q=new Vector3(pos[0]+x,pos[1]+y,pos[2]+z).project(camera);
   assert.ok(Math.abs(q.x)<.99,`cropped x at${f}/${i}`);// Result title ends by484px. Keep8px above and122px clear space before the1470px captions.
   const py=(1-q.y)*960;assert.ok(py>492&&py<1348,`caption/title collision at${f}/${i}: ${py}`);
  }
 }
});
