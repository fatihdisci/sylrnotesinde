import {colors} from '../brand/tokens';
export const MeasurementLine = ({x1, x2, y, progress = 1, color = colors.mutedText}: {
  x1: number; x2: number; y: number; progress?: number; color?: string;
}) => <g fill="none" stroke={color} strokeWidth={2}>
  <path d={`M${x1} ${y-9}V${y+9}M${x1} ${y}H${x1+(x2-x1)*progress}`} />
  <path d={`M${x2} ${y-9}V${y+9}`} opacity={progress} />
</g>;
