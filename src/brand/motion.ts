import {Easing, interpolate} from 'remotion';
export const motion = Object.freeze({label: 12, measurement: 20, camera: 54});
export const ease = Easing.bezier(0.22, 1, 0.36, 1);
export const progress = (frame: number, start: number, duration: number) =>
  interpolate(frame, [start, start + duration], [0, 1], {
    easing: ease, extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
