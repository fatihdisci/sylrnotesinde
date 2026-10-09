import type {ReactNode} from 'react';
import {safeArea, video} from '../brand/tokens';
export type Camera = {x: number; y: number; scale: number};
export const stage = Object.freeze({x: safeArea.left, y: 840, width: video.width - safeArea.left - safeArea.right, height: 560});
export const toScreen = (x: number, y: number, camera: Camera) => ({
  x: stage.width / 2 + (x - camera.x) * camera.scale,
  y: stage.height / 2 + (y - camera.y) * camera.scale,
});
/** Only geometry moves. Legible screen labels live outside this group. */
export const ScaleStage = ({camera, children}: {camera: Camera; children: ReactNode}) =>
  <svg style={{position: 'absolute', left: stage.x, top: stage.y}} width={stage.width} height={stage.height}
    viewBox={`0 0 ${stage.width} ${stage.height}`}>
    <g transform={`translate(${stage.width / 2} ${stage.height / 2}) scale(${camera.scale}) translate(${-camera.x} ${-camera.y})`}>
      {children}
    </g>
  </svg>;
