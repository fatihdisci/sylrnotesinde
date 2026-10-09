import {lerp} from '../../brand/motion';
export type Point = readonly [number,number];
/** Uniform arc-length sampling: one interval is always one million seconds. */
export const resample = (points:readonly Point[],count:number) => {
  const lengths=[0];for(let i=1;i<points.length;i++) lengths.push(lengths[i-1]+Math.hypot(points[i][0]-points[i-1][0],points[i][1]-points[i-1][1]));
  const total=lengths.at(-1)!;let j=1;
  const samples=Array.from({length:count+1},(_,i)=>{
    const d=total*i/count;while(j<lengths.length-1 && lengths[j]<d) j++;
    const p=(d-lengths[j-1])/(lengths[j]-lengths[j-1]);return [lerp(points[j-1][0],points[j][0],p),lerp(points[j-1][1],points[j][1],p)] as Point;
  });
  return {samples,total,unit:total/count};
};
const rawCoil=Array.from({length:24001},(_,i)=>{const t=i/24000,a=-Math.PI/2+t*Math.PI*11,r=70+350*t;return [r*Math.cos(a),r*Math.sin(a)+70] as Point;});
const rawRoad=Array.from({length:24001},(_,i)=>{const t=i/24000;return [650*Math.sin(t*Math.PI*4),t*1800] as Point;});
export const coil=resample(rawCoil,1000);
const roadInitial=resample(rawRoad,1000);
export const road=roadInitial.samples.map(p=>[p[0]*coil.total/roadInitial.total,p[1]*coil.total/roadInitial.total] as Point);
export const days=1_000_000/86400;
export const years=1_000_000_000/(86400*365.25);
export const unitWidth=40;
export const cellPose = (index:number,amount:number) => {
  const a=[lerp(road[index][0],coil.samples[index][0],amount),lerp(road[index][1],coil.samples[index][1],amount)] as Point;
  const b=[lerp(road[index+1][0],coil.samples[index+1][0],amount),lerp(road[index+1][1],coil.samples[index+1][1],amount)] as Point;
  return {x:(a[0]+b[0])/2,y:(a[1]+b[1])/2,angle:Math.atan2(b[1]-a[1],b[0]-a[0]),length:coil.unit};
};
const calendarPath=resample(Array.from({length:2001},(_,i)=>{const t=i/2000;return [504+340*Math.sin(-1.05+t*Math.PI*2.05),610+t*620] as Point;}),11).samples;
export const calendarPose = (index:number) => ({x:calendarPath[index][0],y:calendarPath[index][1],angle:Math.sin(index*.6)*9});
