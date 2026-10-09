import type {ReactNode} from 'react';
import {lerp} from '../brand/motion';
export type Point3 = readonly [number,number,number];
export type SpatialCamera = {target:Point3;scale:number;pitch:number;yaw:number;roll:number;focal:number};
export const project = (p:Point3,c:SpatialCamera,center:readonly [number,number]=[504,920]):readonly [number,number] => {
  const x=p[0]-c.target[0],y=p[1]-c.target[1],z=p[2]-c.target[2];
  const a=c.yaw*Math.PI/180,b=c.pitch*Math.PI/180,r=c.roll*Math.PI/180;
  const xx=x*Math.cos(a)+z*Math.sin(a),zz=-x*Math.sin(a)+z*Math.cos(a);
  const yy=y*Math.cos(b)-zz*Math.sin(b),depth=y*Math.sin(b)+zz*Math.cos(b);
  const perspective=c.focal/Math.max(c.focal*.2,c.focal+depth*c.scale);
  return [center[0]+(xx*Math.cos(r)-yy*Math.sin(r))*c.scale*perspective,center[1]+(xx*Math.sin(r)+yy*Math.cos(r))*c.scale*perspective];
};
export const polygon = (points:readonly (readonly [number,number])[]) => points.map(p=>p.map(n=>n.toFixed(3)).join(',')).join(' ');
export const morphPoints = (a:readonly (readonly [number,number])[],b:readonly (readonly [number,number])[],amount:number) => {
  if(a.length!==b.length) throw new Error('Morph paths require matching point counts');
  return a.map((p,i)=>[lerp(p[0],b[i][0],amount),lerp(p[1],b[i][1],amount)] as const);
};
export const pathFromPoints = (p:readonly (readonly [number,number])[],closed=false) => p.map((v,i)=>`${i?'L':'M'}${v[0].toFixed(3)} ${v[1].toFixed(3)}`).join(' ')+(closed?'Z':'');
/** Masks affect the moving world; captions stay outside this group. */
export const WorldWindow = ({id,children}:{id:string;children:ReactNode}) => <><defs><clipPath id={id}><rect x="36" y="512" width="964" height="815" rx="4"/></clipPath></defs><g clipPath={`url(#${id})`}>{children}</g></>;
