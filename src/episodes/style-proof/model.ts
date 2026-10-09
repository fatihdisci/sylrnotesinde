import {lerp, motion, progress} from '../../brand/motion';
import type {Camera} from '../../components/ScaleStage';
export const units = Object.freeze(Array.from({length: 1000}, (_, i) => {
  const block = Math.floor(i / 100), local = i % 100;
  return Object.freeze({id: i, block, x: (block % 5) * 159 + (local % 10) * 14,
    y: Math.floor(block / 5) * 159 + Math.floor(local / 10) * 14, size: 9});
}));
const cameras: readonly Camera[] = [
  {x: 67.5, y: 4.5, scale: 5.9},
  {x: 67.5, y: 67.5, scale: 3.25},
  {x: 385.5, y: 147, scale: 1.08},
];
export const proofState = (f: number) => {
  const a = progress(f, 90, motion.camera), b = progress(f, 210, 60);
  const desiredCount = f < 210 ? 10 + Math.floor(90 * a) : 100 + Math.floor(900 * b);
  const start = f < 210 ? cameras[0] : cameras[1];
  const end = f < 210 ? cameras[1] : cameras[2];
  const t = f < 210 ? a : b;
  // Interpolate the screen position of the origin, avoiding pan/zoom clipping.
  const scale = lerp(start.scale, end.scale, t);
  const left = lerp(432 - start.x * start.scale, 432 - end.x * end.scale, t);
  const top = lerp(280 - start.y * start.scale, 280 - end.y * end.scale, t);
  const camera = {x: (432 - left) / scale, y: (280 - top) / scale, scale};
  // Reveal only squares fully inside the camera. The counter is the exact visible count.
  let count = 0;
  for (const u of units.slice(0, desiredCount)) {
    if (left + (u.x + u.size) * scale > 864 || top + (u.y + u.size) * scale > 560) break;
    count++;
  }
  return {count, camera,
    groupCount: f < 210 ? 1 : 10, settled: (f >= 144 && f < 210) || f >= 270};
};
