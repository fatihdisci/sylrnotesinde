import {BrandMark} from './BrandMark';
import {colors, safeArea, signatureSpec as s} from './tokens';
/** Shared corner signature; position and size do not come from episode props. */
export const BrandSignature = () =>
  <div data-safe="brand-signature" style={{position: 'absolute', top: safeArea.top + s.topOffset,
    left: safeArea.left, display: 'flex', alignItems: 'center', gap: s.gap}}>
    <BrandMark width={s.width} />
    <span style={{fontSize: s.nameSize, letterSpacing: s.tracking, color: colors.mutedText, fontWeight: 500}}>
      SAYILARIN ÖTESİNDE
    </span>
  </div>;
