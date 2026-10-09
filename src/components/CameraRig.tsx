import type {ReactNode} from 'react';
import {lerp, progress} from '../brand/motion';
export type CameraPose = {x: number; y: number; scale: number};
/** Exponential scale preserves a legible rate across orders of magnitude. */
export const cameraBetween = (frame: number, from: number, duration: number, a: CameraPose, b: CameraPose): CameraPose => {
  const p = progress(frame, from, duration);
  if (p === 0) return a;
  if (p === 1) return b;
  const scale = Math.exp(lerp(Math.log(a.scale),Math.log(b.scale),p));
  // Pan in projected space around the initial anchor. A linear world pan
  // multiplied by a large zoom can throw the anchor out of frame mid-transition.
  const pan = p*b.scale/scale;
  return {x: lerp(a.x,b.x,pan), y: lerp(a.y,b.y,pan), scale};
};
/** Geometry only: subtitles and labels stay in screen coordinates. */
export const CameraRig = ({camera, center = [504,840], children}: {camera: CameraPose; center?: readonly [number,number]; children: ReactNode}) =>
  <g transform={`translate(${center[0]} ${center[1]}) scale(${camera.scale}) translate(${-camera.x} ${-camera.y})`}>{children}</g>;
