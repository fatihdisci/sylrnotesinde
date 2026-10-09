import {AbsoluteFill} from 'remotion';
import {colors, safeArea as s} from '../brand/tokens';
export const SafeAreaDebug = () => <AbsoluteFill style={{pointerEvents: 'none'}}>
  <div style={{position: 'absolute', left: s.left, right: s.right, top: s.top, bottom: s.bottom,
    border: `2px dashed ${colors.secondaryAccent}`, color: colors.secondaryAccent, fontSize: 28}}>
    AYARLANABİLİR GÜVENLİ ALAN · ÖNİZLEME
  </div>
</AbsoluteFill>;
