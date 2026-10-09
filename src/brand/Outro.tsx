import {AbsoluteFill, Html5Audio, staticFile, useCurrentFrame} from 'remotion';
import {BrandMark} from './BrandMark';
import {progress} from './motion';
import {colors, outroSpec as o, safeArea, typography} from './tokens';
/** Intentionally no props. Episodes cannot override geometry, duration, sound or type. */
export const Outro = () => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{backgroundColor: colors.background, color: colors.foreground, fontFamily: typography.sans}}>
    <div style={{position: 'absolute', left: safeArea.left, right: safeArea.right, top: 800, textAlign: 'center'}}>
      <BrandMark width={o.markWidth} lines={progress(f + 1, 0, o.lineEnd)} marker={progress(f + 1, o.markerStart, o.markerEnd - o.markerStart)} />
      <div data-safe="outro-name" style={{marginTop: 64, fontSize: o.nameSize, fontWeight: 500, letterSpacing: 3,
        opacity: progress(f, 3, o.nameEnd - 3)}}>SAYILARIN ÖTESİNDE</div>
    </div>
    <Html5Audio src={staticFile(o.audio)} />
  </AbsoluteFill>;
};
