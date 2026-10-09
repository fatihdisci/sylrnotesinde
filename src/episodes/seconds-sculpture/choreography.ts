import type {Episode} from '../types';
export type V3 = [number,number,number];
export const mix=(a:number,b:number,t:number)=>a+(b-a)*t;
export const clamp=(x:number)=>Math.max(0,Math.min(1,x));
export const ease=(t:number)=>{t=clamp(t);return t*t*t*(t*(t*6-15)+10);};
export const phase=(f:number,a:number,b:number)=>ease((f-a)/(b-a));
export const anchor=(episode:Episode,id:string)=>{const e=episode.direction?.events.find(e=>e.id===id);if(!e)throw new Error(`Missing choreography anchor ${id}`);return e.from;};
export const lerp3=(a:V3,b:V3,t:number):V3=>[mix(a[0],b[0],t),mix(a[1],b[1],t),mix(a[2],b[2],t)];
/** 1000 identical, unit-sized solids. Assembly paths are schematic, never an area ratio. */
export const lattice=(i:number):V3=>[(i%10-4.5)*1.06,(Math.floor(i/10)%10-4.5)*1.06,(Math.floor(i/100)-4.5)*1.06];
export function blockPose(i:number,f:number,e:Episode):{position:V3;rotation:V3;scale:number}{
 const launch=anchor(e,'launch'),travel=anchor(e,'travel'),lock=anchor(e,'thousand'),compare=anchor(e,'compare');
 const x=i%10,y=Math.floor(i/10)%10,z=Math.floor(i/100);
 const goal=lattice(i);
 // A receding corridor of equal solids; the camera starts in front of its first unit.
 const twist=(9-z)*.13,dx=(x-4.5)*2.1,dy=(y-4.5)*2.1;
 const corridor:V3=[dx*Math.cos(twist)-dy*Math.sin(twist)-9.45,dx*Math.sin(twist)+dy*Math.cos(twist)-9.45,-(9-z)*5.2];
 const order=(9-z)*7+(9-x)+(9-y);
 const reveal=i===999?1:phase(f,launch+order*.25,travel+64+order*.2);
 const gather=phase(f,lock-30+z,lock+28+z);
 let position=lerp3(corridor,goal,gather);
 // The mass is already behind the source before the dolly; fog/distance reveal it without a pop.
 if(i!==999)position[2]-=50*(1-phase(f,launch-16,launch+35));
 const drift=(1-gather)*(1-reveal)*.3;
 position=[position[0]+Math.sin(i*2.1)*drift,position[1]+Math.cos(i*1.7)*drift,position[2]];
 const section=phase(f,anchor(e,'years'),compare+24);
 position[1]+=(y-4.5)*.22*section;
 position[0]+=Math.sin(y*.45)*.35*section;
 const pull=phase(f,compare,compare+58);
 // Source is an actual member of the1000, removed from its corner, not duplicated.
 if(i===999)position=lerp3(position,[-8,0,7.2],pull);
 return {position,rotation:[(1-gather)*.18*Math.sin(i), (1-gather)*.22*Math.cos(i),0],scale:1};
}
export function cameraPose(f:number,e:Episode):{eye:V3;target:V3;fov:number}{
 const a=(id:string)=>anchor(e,id);
 const keys:{f:number;eye:V3;target:V3;fov:number}[]=[
 {f:0,eye:[.8,.55,1.8],target:[0,0,0],fov:42},
 {f:20,eye:[2.1,1.35,3.3],target:[0,0,0],fov:42},
 {f:a('shock'),eye:[2.8,2.1,5.2],target:[0,0,0],fov:42},
 {f:a('shock')+38,eye:[11,6,21],target:[0,0,-3],fov:44},
 {f:a('zeros'),eye:[8,3,15],target:[0,0,-2],fov:44},
 {f:a('dive'),eye:[3.2,1.5,6.2],target:[0,0,0],fov:40},
 {f:a('clock'),eye:[1.5,2.1,11.7],target:[0,0,0],fov:42},
 {f:a('unwind'),eye:[-1.9,1.6,11.7],target:[0,0,0],fov:44},
 {f:a('calendar'),eye:[4.1,3.5,15.5],target:[0,0,0],fov:44},
 {f:a('million'),eye:[3,2.4,21],target:[0,-.6,0],fov:44},
 {f:a('fraction')+40,eye:[-2.5,3,20.5],target:[0,-.5,0],fov:44},
 {f:a('collect'),eye:[-2.4,2.7,20.5],target:[0,-.4,0],fov:42},
 {f:a('block')+32,eye:[2.5,1.8,4.5],target:[0,0,0],fov:42},
 {f:a('launch'),eye:[1.9,1.2,3.7],target:[0,0,0],fov:42},
 {f:a('travel'),eye:[9,5,16],target:[-6,-6,-15],fov:52},
 {f:a('sample'),eye:[19,12,29],target:[-6,-6,-15],fov:52},
 {f:a('thousand')-20,eye:[18,11,29],target:[-6,-6,-15],fov:52},
 {f:a('thousand')+58,eye:[22,16,32],target:[0,0,0],fov:44},
 {f:a('years')+24,eye:[-21,11,37],target:[0,-1,0],fov:44},
 {f:a('compare'),eye:[-21,12,37],target:[0,-1,0],fov:44},
 {f:a('extend'),eye:[-23,12,38],target:[-1,-1.4,1],fov:44},
 {f:a('impact'),eye:[-22,13,39],target:[-1,-1.4,1],fov:44},
 {f:e.durationInFrames-45,eye:[-21.5,13,39],target:[-1,-1.4,1],fov:44},
 ];
 const b=keys.findIndex(k=>k.f>f);if(b<0)return keys.at(-1)!;if(b===0)return keys[0];
 const p=keys[b-1],q=keys[b],t=phase(f,p.f,q.f);
 return {eye:lerp3(p.eye,q.eye,t),target:lerp3(p.target,q.target,t),fov:mix(p.fov,q.fov,t)};
}
