/** Brand candidate. Changes require an explicit user request. */
export const BRAND_VERSION = '0.1-candidate' as const;
export const colors = Object.freeze({
  background: '#111615', foreground: '#F2F0E9', accent: '#F07857',
  secondaryAccent: '#9DBFCA', mutedText: '#909B97', guideLine: '#35413E',
});
export const video = Object.freeze({width: 1080, height: 1920, fps: 30});
/** Editorial starting margins; not official platform specifications. */
export const safeArea = Object.freeze({left: 72, right: 144, top: 180, bottom: 300});
export const typography = Object.freeze({
  sans: 'IBM Plex Sans', mono: 'IBM Plex Mono',
  number: 200, title: 88, caption: 46, measure: 36,
});
export const markGeometry = Object.freeze({
  lengths: Object.freeze([24, 40, 64]), spacing: 10, stroke: 3, marker: 6,
  width: 74, height: 26,
});
export const signatureSpec = Object.freeze({width: 64, topOffset: 4, gap: 22, nameSize: 26, tracking: 3});
export const outroSpec = Object.freeze({
  frames: 45, lineEnd: 12, markerStart: 12, markerEnd: 24, nameEnd: 20,
  markWidth: 222, nameSize: 52, audio: 'audio/brand/closing.wav',
});
