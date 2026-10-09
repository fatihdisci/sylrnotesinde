import {colors} from '../../brand/tokens';
import {lerp} from '../../brand/motion';
import type {CameraPose} from '../../components/CameraRig';
export const ribbonCell = (index:number) => {
  const length=1_000_000/(86400*365.25)*80, rowWidth=640;
  const start=index*length,row=Math.floor(start/rowWidth),x=start%rowWidth;
  const first=Math.min(length,rowWidth-x);
  return {row,x,first,second:length-first};
};
/** Same thousand million-second cells unfold onto a linear, folded year axis.
 * A cell straddling a row is split, retaining its exact total length. */
export const TimeRibbon = ({camera,amount,group}: {camera:CameraPose;amount:number;group:number}) => {
  return <g>{Array.from({length:1000},(_,i)=>{
    const col=i%25,row=Math.floor(i/25);
    const x0=504+(col*24+Math.floor(col/5)*32*group-camera.x)*camera.scale;
    const y0=930+(row*24+Math.floor(row/20)*32*group-camera.y)*camera.scale;
    const {row:r,x,first,second}=ribbonCell(i);
    const color=i===0?colors.accent:colors.secondaryAccent;
    return <g key={i}>
      <rect x={lerp(x0,184+x,amount)} y={lerp(y0,640+r*170,amount)} width={lerp(20*camera.scale,first,amount)} height={lerp(20*camera.scale,100,amount)} fill={color}/>
      {second>0 && <rect x="184" y={640+(r+1)*170} width={second} height="100" fill={color} opacity={amount}/>}
    </g>;
  })}
  {amount>.99 && <g fill={colors.mutedText} fontSize="34">
    {Array.from({length:4},(_,row)=><g key={row}>
      <path d={`M184 ${632+row*170}H824`} stroke={colors.guideLine} strokeWidth="2"/>
      {Array.from({length:9},(_,i)=><path key={i} d={`M${184+i*80} ${622+row*170}v18`} stroke={colors.foreground} strokeWidth="2"/>)}
      <text data-safe={`year-${row}`} x="184" y={610+row*170}>{row*8} yıl</text>
    </g>)}
    <path d="M184 640V740 M184 690H112" stroke={colors.accent} strokeWidth="3"/>
    <text data-safe="ribbon-first-unit" x="84" y="667" fill={colors.accent}>1</text>
    <text data-safe="ribbon-end" x="824" y="1260" textAnchor="end" fill={colors.secondaryAccent}>≈ 31,7 yıl</text>
  </g>}
  </g>;
};
