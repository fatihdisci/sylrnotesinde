import {useCurrentFrame} from 'remotion';
import type {Episode} from '../types';
import {colors as c,typography} from '../../brand/tokens';
import {lerp,progress} from '../../brand/motion';
import {EpisodeComposition} from '../../components/EpisodeComposition';
import {CaptionTrack} from '../../components/CaptionTrack';
import {eventFrames} from '../../components/AudioDirection';
import {project,polygon,morphPoints,pathFromPoints,WorldWindow,type SpatialCamera,type Point3} from '../../components/SpatialMotion';
import {calendarPose,cellPose,days,unitWidth,years} from './geometry';

type Frames=Record<string,number>;
const span=(f:number,a:number,b:number)=>progress(f,a,Math.max(1,b-a));
const smooth=(f:number,a:number,b:number)=>{const p=Math.max(0,Math.min(1,(f-a)/Math.max(1,b-a)));return p*p*(3-2*p);};
const mono={fontFamily:typography.mono};
const heading={position:'absolute' as const,left:72,width:864,lineHeight:1.04,fontWeight:500};

const Clock = ({f,e}:{f:number;e:Frames}) => {
  const dive=span(f,e.dive,e.clock),open=span(f,e.unwind,e.calendar);
  const surprise=span(f,e.shock,e.zeros)*(1-span(f,e.zeros,e.dive));
  const opening=span(f,e.hook,e.shock);
  const size=lerp(lerp(1.58,.90,opening),1.02,dive)-surprise*.24;
  const cx=lerp(470,504,dive)-surprise*90,cy=lerp(960,945,dive);
  const angle=f*6; // One revolution per2s: an explicitly accelerated minute.
  return <g opacity={1-open} transform={`translate(${cx} ${cy}) rotate(${lerp(-13,0,dive)}) scale(${size})`}>
    {/* The visible side is the clock's casing, not an unrelated decorative ring. */}
    <ellipse cy="24" rx="343" ry="347" fill={c.guideLine}/>
    <circle r="343" fill={c.background} stroke={c.foreground} strokeWidth="3"/>
    <circle r="327" fill="none" stroke={c.accent} strokeWidth="11"/>
    <circle r="295" fill="none" stroke={c.guideLine} strokeWidth="2"/>
    {Array.from({length:60},(_,i)=>{
      const a=i*Math.PI/30;return <path key={i} d={`M${Math.sin(a)*312} ${-Math.cos(a)*312}L${Math.sin(a)*(i%5?301:280)} ${-Math.cos(a)*(i%5?301:280)}`} stroke={i%5?c.guideLine:c.foreground} strokeWidth={i%5?2:5}/>;
    })}
    {[0,3,6,9].map(h=><text key={h} x={Math.sin(h*Math.PI/6)*238} y={-Math.cos(h*Math.PI/6)*238+15} textAnchor="middle" fill={c.foreground} fontSize="44" fontFamily={typography.mono}>{h===0?'60':h*5}</text>)}
    <path d="M0 28V-225" stroke={c.accent} strokeWidth="6" transform={`rotate(${angle})`}/>
    <path d="M0 0V-145" stroke={c.foreground} strokeWidth="13" strokeLinecap="round" transform={`rotate(${angle/60})`}/>
    <circle r="13" fill={c.accent}/>
    <text y="155" textAnchor="middle" fill={c.mutedText} fontSize="29" fontFamily={typography.mono}>SANİYE</text>
  </g>;
};

const Calendar = ({f,e}:{f:number;e:Frames}) => {
  const unfold=span(f,e.unwind,e.million),fill=span(f,e.million,e.fraction),fraction=span(f,e.fraction,e.collect);
  const pack=span(f,e.collect,e.block),seal=span(f,e.block,e.launch);
  const focus=fraction*(1-pack),track=span(f,e.calendar,e.million);
  const centers=Array.from({length:12},(_,i)=>calendarPose(i));
  const clockPath=Array.from({length:61},(_,i)=>[504+315*Math.sin(i/60*Math.PI*2),945-315*Math.cos(i/60*Math.PI*2)] as const);
  const ribbonPath=Array.from({length:61},(_,i)=>{const t=i/60;return [504+340*Math.sin(-1.05+t*Math.PI*2.05),610+t*620] as const;});
  return <g opacity={1-seal} transform={`translate(0 ${Math.sin(track*Math.PI)*28})`}>
    <path d={pathFromPoints(morphPoints(clockPath,ribbonPath,unfold))} fill="none" stroke={c.guideLine} strokeWidth={lerp(3,28,unfold)} opacity={1-pack}/>
    {centers.map((p,i)=>{
      const a=i*Math.PI/6,stagger=span(f,e.unwind+i*2,e.million-(11-i)*2);
      const x=lerp(504+Math.sin(a)*300,p.x,stagger),y=lerp(945-Math.cos(a)*300,p.y,stagger);
      const px=lerp(i===11?lerp(x,746,focus):x,504+(i-6)*2,pack),py=lerp(i===11?lerp(y,1110,focus):y,945+(11-i)*3,pack);
      const w=lerp(7,90,stagger),h=lerp(20,112,stagger);
      const extent=i<11?Math.min(1,Math.max(0,fill*11-i)):fraction*(days-11);
      return <g key={i} transform={`translate(${px} ${py}) rotate(${lerp(p.angle*stagger,8,pack)}) scale(${lerp(i===11?lerp(1,1.8,focus):1,1.8,pack)})`}>
        <defs><clipPath id={`day-${i}`}><rect x={-w/2} y={-h/2} width={w} height={h} rx="5"/></clipPath></defs>
        <rect x={-w/2+3} y={-h/2+7} width={w} height={h} rx="5" fill={c.guideLine}/>
        <rect x={-w/2} y={-h/2} width={w} height={h} rx="5" fill={c.foreground}/>
        <g clipPath={`url(#day-${i})`}>
          <rect x={-w/2} y={h/2-h*extent} width={w} height={h*extent} fill={c.accent}/>
          <path d={`M${-w/2} ${-h/2+30}H${w/2}`} stroke={c.background} strokeWidth="2" opacity=".4"/>
        </g>
        {stagger>.65 && <g fill={c.background} opacity={span(stagger,.65,1)}>
          <circle cx={-w*.27} cy={-h/2+12} r="4"/><circle cx={w*.27} cy={-h/2+12} r="4"/>
          <text y="18" textAnchor="middle" fontSize="44" fontFamily={typography.mono}>{String(i+1).padStart(2,'0')}</text>
          <text y="48" textAnchor="middle" fontSize="17" letterSpacing="3">GÜN</text>
        </g>}
      </g>;
    })}
  </g>;
};

const cameraAt = (f:number,e:Frames):SpatialCamera => {
  if(f<e.sample){
    const p=smooth(f,e.launch,e.sample),scale=Math.exp(lerp(Math.log(32),Math.log(.56),p)),track=500*p*.56/scale;
    const i=Math.floor(track),a=cellPose(i,0),b=cellPose(Math.min(999,i+1),0);
    return {target:[lerp(a.x,b.x,track-i),lerp(a.y,b.y,track-i),0],scale,pitch:lerp(60,22,p),yaw:lerp(-8,14,p),roll:lerp(-8,12,p),focal:3200};
  }
  if(f<e.thousand){
    const p=smooth(f,e.sample,e.thousand),scale=Math.exp(lerp(Math.log(.56),Math.log(7),p)),focus=cellPose(420,0),overview=cellPose(500,0);
    return {target:[focus.x-(focus.x-overview.x)*.56*(1-p)/scale,focus.y-(focus.y-overview.y)*.56*(1-p)/scale,0],scale,pitch:lerp(22,48,p),yaw:14,roll:lerp(12,-12,p),focal:3200};
  }
  const p=smooth(f,e.thousand,e.billion),scale=Math.exp(lerp(Math.log(7),Math.log(.91),p)),focus=cellPose(420,p),pan=p*.91/scale,top=span(f,e.years,e.compare);
  return {target:[lerp(focus.x,0,pan),lerp(focus.y,70,pan),0],scale,pitch:lerp(lerp(48,14,p),0,top),yaw:lerp(14,0,p),roll:lerp(-12,0,p),focal:3200};
};

const TimeRoad = ({f,e,preview=false}:{f:number;e:Frames;preview?:boolean}) => {
  const curl=preview?1:smooth(f,e.thousand,e.billion),cam=preview?{target:[0,70,0] as Point3,scale:1.12,pitch:28,yaw:-14,roll:14,focal:2600}:cameraAt(f,e);
  const showAll=preview||f>=e.launch,visible=showAll?1000:1;
  const yearsP=span(f,e.years,e.compare),trace=span(f,e.extend,e.impact);
  const count=span(f,e.launch,e.sample),cover=1-span(f,e.launch,e.travel);
  const first=cellPose(0,curl),firstScreen=project([first.x,first.y,0],cam);
  return <g opacity={preview?.32:1}>
    {Array.from({length:visible},(_,i)=>{
      const pose=cellPose(i,curl),cos=Math.cos(pose.angle),sin=Math.sin(pose.angle),gap=.07;
      const half=pose.length*(1-gap)/2;
      const corner=(x:number,y:number,z:number):Point3=>[pose.x+x*cos-y*sin,pose.y+x*sin+y*cos,z];
      const corners=[corner(-half,-unitWidth/2,0),corner(half,-unitWidth/2,0),corner(half,unitWidth/2,0),corner(-half,unitWidth/2,0)];
      const points=corners.map(p=>project(p,cam));
      if(points.every(p=>p[0]<20)||points.every(p=>p[0]>1000)||points.every(p=>p[1]<240)||points.every(p=>p[1]>1450)) return null;
      const opacity=i===0?1:preview?1:Math.min(1,Math.max(0,count*1300-i*.3));
      const shade=i===0||(i===420&&f>=e.sample&&f<e.thousand)?c.accent:Math.floor(i/100)%2?c.foreground:c.secondaryAccent;
      const depth=[points[2],points[3],project(corner(-half,unitWidth/2,1.2),cam),project(corner(half,unitWidth/2,1.2),cam)];
      return <g key={i} opacity={opacity}>
        {cam.scale>1 && <polygon points={polygon(depth)} fill={c.guideLine}/>}
        <polygon points={polygon(points)} fill={shade} opacity={f>=e.extend && i>trace*999?lerp(1,.38,span(f,e.extend,e.extend+18)):1}/>
        {cam.scale>5 && <path d={pathFromPoints([points[0],points[1]])} stroke={c.foreground} strokeWidth="1.4" opacity=".45"/>}
      </g>;
    })}
    {!preview && f<e.travel && <g opacity={cover} transform={`translate(${firstScreen[0]} ${firstScreen[1]}) rotate(-8)`} fill={c.background} textAnchor="middle">
      <text y="-18" fontSize={Math.min(30,cam.scale*.94)} fontFamily={typography.mono}>1.000.000</text>
      <text y="27" fontSize={Math.min(30,cam.scale*.94)}>saniye</text>
    </g>}
    {!preview && yearsP>0 && Array.from({length:32},(_,year)=>{
      if(year>yearsP*31) return null;
      const index=Math.min(999,Math.round(year/years*1000)),pose=cellPose(index,1),r=Math.hypot(pose.x,pose.y-70);
      const x=pose.x/r,y=(pose.y-70)/r;
      const a=project([pose.x+x*9,pose.y+y*9,0],cam),b=project([pose.x+x*17,pose.y+y*17,0],cam);
      return <path key={year} d={pathFromPoints([a,b])} stroke={c.accent} strokeWidth="2"/>;
    })}
    {!preview && f>=e.compare && <g>
      <path d={`M${firstScreen[0]} ${firstScreen[1]}V892`} fill="none" stroke={c.accent} strokeWidth="2"/>
      <circle cx={firstScreen[0]} cy={firstScreen[1]} r="4" fill={c.accent}/>
      <text data-safe="first-segment" x="504" y="938" textAnchor="middle" fill={c.accent} fontSize="44" fontFamily={typography.mono}>1</text>
    </g>}
  </g>;
};

export const SecondsAudioFirst = ({episode,hideCaptions=false,debug=false}:{episode:Episode;hideCaptions?:boolean;debug?:boolean}) => {
  const f=useCurrentFrame();if(!episode.direction) throw new Error('Audio-first scene requires a resolved storyboard');
  const e=eventFrames(episode.direction),cal=f>=e.unwind&&f<e.launch,roadOn=f>=e.collect;
  const pack=span(f,e.collect,e.block),intro=span(f,e.shock,e.zeros)*(1-span(f,e.zeros,e.dive));
  const title=f<e.shock?'Bir milyon.':f<e.zeros?'Bir milyar?':f<e.dive?'Sadece\nüç sıfır.':f<e.clock?'Geçen zamana\nbakın.':f<e.unwind?'Her turda\nbir dakika.':f<e.million?'Zaman\naçılıyor.':f<e.collect?'≈ 11,6 gün':f<e.launch?'Zamanı\nbirleştirelim.':f<e.sample?'Ölçeği\nbüyütelim.':f<e.thousand?'Aynı birim.\nÇok daha fazlası.':f<e.billion?'1.000\neşit blok.':f<e.compare?'≈ 31,7 yıl':'11,6 gün.\n31,7 yıl.';
  const large=(f>=e.million&&f<e.collect)||(f>=e.billion&&f<e.compare);
  const measurement=f<e.unwind?'Hızlandırılmış saat · 1 tur = 1 dakika':f<e.collect?(f>=e.fraction?'11 tam gün + günün %57,4’ü':'Saat işaretlerinden takvim yapraklarına'):f<e.launch?'1 blok = 1 milyon saniye':f<e.thousand?'Her blok 1 milyon saniye':f<e.compare?'1.000 eşit birim · yaklaşık 31,7 yıl':f<e.impact?'Aynı ölçekte · 1 birim ve 1.000 birim':'Tam 1.000 kat.';
  return <EpisodeComposition episode={episode} debug={debug}>
    <svg width="1080" height="1920" viewBox="0 0 1080 1920" style={{position:'absolute',inset:0}}>
      <WorldWindow id="time-world">
        {intro>0 && <g opacity={intro}><TimeRoad f={f} e={e} preview/></g>}
        {f<e.million && <Clock f={f} e={e}/>}
        {roadOn && <g opacity={pack}><TimeRoad f={f} e={e}/></g>}
        {cal && <Calendar f={f} e={e}/>}
      </WorldWindow>
    </svg>
    <div data-safe="heading" style={{...heading,top:large?304:286,fontSize:large?128:f>=e.sample&&f<e.thousand?76:88,whiteSpace:'pre-line',color:f>=e.million&&f<e.collect?c.accent:c.foreground,...(large?mono:{})}}>{title}</div>
    <div data-safe="measurement" style={{...heading,top:f>=e.impact?1326:1342,fontSize:f>=e.impact?76:34,color:f>=e.impact?c.accent:c.secondaryAccent,...(f>=e.impact?mono:{})}}>{measurement}</div>
    {((f>=e.fraction&&f<e.collect)||(f>=e.launch&&f<e.impact)) && <div data-safe="scale-note" style={{...heading,top:1400,fontSize:30,color:c.mutedText}}>{f<e.collect?'12. günün ayrıntısı · yakın plan':f>=e.compare?'Şematik yol · aynı uzunlukta 1.000 zaman birimi':'Şematik zaman şeridi · perspektifli görünüş'}</div>}
    {!hideCaptions && <CaptionTrack cues={episode.captions}/>}
  </EpisodeComposition>;
};
