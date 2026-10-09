import {colors, markGeometry as g} from './tokens';
export const BrandMark = ({width = 74, lines = 1, marker = 1}: {
  width?: number; lines?: number; marker?: number;
}) => <svg width={width} height={width * g.height / g.width} viewBox={`0 0 ${g.width} ${g.height}`} aria-label="Sayıların Ötesinde ölçüm işareti">
  {g.lengths.map((length, i) => <line key={length} x1={1.5} x2={1.5 + length * lines}
    y1={3 + i * g.spacing} y2={3 + i * g.spacing} stroke={colors.foreground} strokeWidth={g.stroke} />)}
  <rect x={68} y={20 - (1 - marker) * 8} width={g.marker} height={g.marker}
    fill={colors.accent} opacity={marker} />
</svg>;
