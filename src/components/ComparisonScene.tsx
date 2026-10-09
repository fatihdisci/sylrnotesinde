import type {ReactNode} from 'react';
import {colors, safeArea, typography} from '../brand/tokens';
/** Neutral stage primitive, not a card layout. Explicit encoding must be supplied. */
export const ComparisonScene = ({children, encoding}: {children: ReactNode; encoding: string}) =>
  <><div style={{position: 'absolute', inset: 0}}>{children}</div>
    <div data-safe="encoding" style={{position: 'absolute', left: safeArea.left, top: 780,
      font: `400 ${typography.measure}px '${typography.sans}'`, color: colors.mutedText}}>{encoding}</div></>;
