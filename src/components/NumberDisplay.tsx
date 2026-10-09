import {colors, typography} from '../brand/tokens';
export const formatTR = (value: number, decimals = 0) => new Intl.NumberFormat('tr-TR', {
  minimumFractionDigits: decimals, maximumFractionDigits: decimals,
}).format(value);
export const NumberDisplay = ({value, size = typography.number}: {value: number; size?: number}) =>
  <span style={{fontFamily: typography.mono, fontSize: size, fontWeight: 500, fontVariantNumeric: 'tabular-nums',
    letterSpacing: -8, lineHeight: 1, color: colors.foreground}}>{formatTR(value)}</span>;
export const Counter = NumberDisplay;
