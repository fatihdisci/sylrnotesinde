import {colors} from '../brand/tokens';
import {lerp, progress} from '../brand/motion';
/** Equal cells encode COUNT, never area/length. A partial day uses a partial cell. */
export const QuantityField = ({count, columns, pitch, size, frame, from, duration, regroup = 0, groupShape = [10,10], leadOpacity = 1}: {
  count: number; columns: number; pitch: number; size: number; frame: number; from: number; duration: number; regroup?: number; leadOpacity?: number; groupShape?: readonly [number,number];
}) => <g>{Array.from({length: Math.ceil(count)}, (_,i) => {
  const col=i%columns, row=Math.floor(i/columns);
  const p=progress(frame,from+duration*i/Math.max(1,count-1),12);
  const fraction=Math.min(1,count-i);
  // Regroup cells without changing their individual sizes, while retaining each cell's identity.
  const x=lerp(col*pitch,col*pitch+(Math.floor(col/groupShape[0])*32),regroup);
  const y=lerp(row*pitch,row*pitch+Math.floor(row/groupShape[1])*32,regroup);
  return <rect key={i} x={x} y={y} width={size*fraction} height={size} rx={size*.06} fill={i===0 ? colors.accent : colors.secondaryAccent} opacity={i===0 ? leadOpacity : p} />;
})}</g>;
