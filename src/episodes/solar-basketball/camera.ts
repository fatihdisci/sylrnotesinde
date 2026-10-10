import type {Episode} from '../types';
import {positions,scaleModel,type V3} from './model';
export const mix=(a:number,b:number,p:number)=>a+(b-a)*p;
export const smooth=(v:number)=>{const p=Math.max(0,Math.min(1,v));return p*p*p*(10+p*(-15+p*6));};
export const phase=(f:number,a:number,b:number)=>smooth((f-a)/Math.max(1,b-a));
export const blend=(a:V3,b:V3,p:number):V3=>a.map((v,i)=>mix(v,b[i],p)) as V3;
export const anchor=(e:Episode,id:string)=>{const item=e.direction?.events.find(x=>x.id===id);if(!item)throw new Error('Missing solar event: '+id);return item.from;};
export type Pose={eye:V3;target:V3;fov:number};
const around=(target:V3,distance:number,angle:number,elevation=.2,fov=42):Pose=>({target,eye:[target[0]+Math.sin(angle)*distance,target[1]+elevation*distance,target[2]+Math.cos(angle)*distance],fov});
const interpolate=(a:Pose,b:Pose,p:number):Pose=>({eye:blend(a.eye,b.eye,p),target:blend(a.target,b.target,p),fov:mix(a.fov,b.fov,p)});
export const cameraPose=(f:number,e:Episode):Pose=>{
 const a=(id:string)=>anchor(e,id),earth=positions.earth,moon=positions.moon;
 const mid:V3=[scaleModel.moon.distance/2,1.3,earth[2]];
 if(f<a('earth-size'))return around(positions.sun,mix(.185,.72,phase(f,0,72)),mix(-.28,.38,phase(f,0,a('earth-size'))),.12);
 if(f<a('distance-shock'))return around(earth,mix(.0065,.0095,phase(f,a('earth-size'),a('pin')+35)),mix(-.6,.35,phase(f,a('earth-size'),a('distance-shock'))),.12,44);
 if(f<a('street')){
  const p=phase(f,a('distance-shock'),a('street')),d=Math.exp(mix(Math.log(.0095),Math.log(40),p));
  // Keep the tiny Earth on the optical axis until the camera is far enough
  // to reframe the street; moving the target early would leave a blank macro.
  const target=blend(earth,[0,1.3,-12.9],smooth(Math.max(0,(d-15)/25)));
  return around(target,d,mix(.35,.42,p),mix(.12,.65,p),mix(44,53,p));
 }
 if(f<a('arrival')){
  const p=phase(f,a('street'),a('arrival'));
  // Single continuous dolly from a high establish to the 25.8 m street destination.
  const start=around([0,1.3,-12.9],40,.42,.65,53);
  return interpolate(start,{eye:[2.1,3.4,earth[2]+8],target:earth,fov:48},p);
 }
 if(f<a('moon')){
  const p=phase(f,a('arrival'),a('moon'));
  const d=Math.exp(mix(Math.log(8.5),Math.log(.0065),p));
  return around(earth,d,mix(.26,-.35,p),mix(.25,.12,p),mix(48,44,p));
 }
 if(f<a('moon-size')){
  const p=phase(f,a('moon'),a('moon-range')+34);
  return {eye:blend(around(earth,.0065,-.35,.12,44).eye,[mid[0]-.006,1.32,earth[2]+.22],p),target:blend(earth,mid,p),fov:44};
 }
 if(f<a('jupiter')){
  const p=phase(f,a('moon-size'),a('moon-size')+22),returnP=phase(f,a('jupiter')-27,a('jupiter'));
  const detail=around(moon,.0022,.1+.12*phase(f,a('moon-size'),a('jupiter')),.1,44);
  return interpolate(detail,{eye:[mid[0]+.006,1.32,earth[2]+.22],target:mid,fov:44},Math.max(1-p,returnP));
 }
 if(f<a('jup-road'))return around(positions.jupiter,mix(.065,.081,phase(f,a('jupiter'),a('jup-road'))),mix(-.48,.42,phase(f,a('jupiter'),a('jup-road'))),.18,42);
 if(f<a('neptune')){
  const p=phase(f,a('jup-road'),a('neptune'));
  const distance=mix(scaleModel.earth.distance,scaleModel.jupiter.distance,p);
  return {eye:[mix(1.8,3.5,p),mix(2.4,5.5,p),-distance+10],target:[0,1.3,-distance-10],fov:58};
 }
 if(f<a('far-flight'))return around(positions.neptune,mix(.022,.03,phase(f,a('neptune'),a('far-flight'))),mix(-.4,.32,phase(f,a('neptune'),a('far-flight'))),.15,44);
 if(f<a('neighborhood')){
  const p=phase(f,a('far-flight'),a('neighborhood'));
  const distance=mix(scaleModel.jupiter.distance,scaleModel.neptune.distance,p);
  return {eye:[mix(2,12,p),mix(3.5,42,p),-distance+22],target:[0,mix(1.3,0,p),-distance-32],fov:58};
 }
 const start:Pose={eye:[12,42,-scaleModel.neptune.distance+22],target:[0,0,-scaleModel.neptune.distance-32],fov:58};
 const end:Pose={eye:[40,1700,180],target:[0,0,-330],fov:58};
 const p=phase(f,a('neighborhood'),a('whole')+50);
 const out=interpolate(start,end,p);
 const coast=phase(f,a('whole')+50,e.durationInFrames-45);
 out.eye[0]+=coast*100;out.eye[1]+=coast*45;return out;
};
