import {useCurrentFrame} from 'remotion';
import type {Episode} from '../types';
import {colors, typography} from '../../brand/tokens';
import {lerp, progress} from '../../brand/motion';
import {CaptionTrack} from '../../components/CaptionTrack';
import {EpisodeComposition} from '../../components/EpisodeComposition';
import {CameraRig, cameraBetween} from '../../components/CameraRig';
import {TimeRibbon} from './TimeRibbon';
import {QuantityField} from '../../components/QuantityField';
import {EventSoundTrack, type SoundEvent} from '../../components/EventSoundTrack';
import {days, filmEvents} from './model';

const labelStyle = {position:'absolute' as const,left:72,width:864};
export const SecondsFilm = ({episode,hideCaptions=false,debug=false}: {episode:Episode;hideCaptions?:boolean;debug?:boolean}) => {
  const f=useCurrentFrame(), e=filmEvents(episode), study=episode.kind==='motion-study';
  const dayP=progress(f,e.days,study?28:70), packP=progress(f,e.pack,study?20:48);
  const zoomP=progress(f,e.zoom,study?72:140), groupP=progress(f,e.group,36);
  const ribbonP=e.ribbon===null?0:progress(f,e.ribbon,54);
  const resultP=progress(f,e.result,30);
  const field=f>=e.pack;
  // One cell is carried out of the calendar. Zoom reveals 999 cells already in the world.
  const baseCamera=cameraBetween(f,e.zoom,study?72:140,{x:10,y:10,scale:24},{x:300,y:480,scale:.76});
  const camera={...baseCamera,x:baseCamera.x+64*groupP,y:baseCamera.y+16*groupP};
  const events:SoundEvent[]=[
    ...Array.from({length:Math.ceil(e.days/30)},(_,i)=>({id:`tick-${i}`,frame:i*30,path:'audio/motion/tick.wav',durationInFrames:6,gain:i===0?.20:.07})),
    {id:'days',frame:e.days,path:'audio/motion/unfold.wav',durationInFrames:18,gain:.14},
    {id:'pack',frame:e.pack,path:'audio/motion/merge.wav',durationInFrames:18,gain:.16},
    {id:'zoom',frame:e.zoom,path:'audio/motion/depth.wav',durationInFrames:36,gain:.17},
    {id:'group',frame:e.group,path:'audio/motion/settle.wav',durationInFrames:15,gain:.16},
    {id:'years',frame:e.years,path:'audio/motion/reveal.wav',durationInFrames:24,gain:.12},
    {id:'result',frame:e.result,path:'audio/motion/reveal.wav',durationInFrames:24,gain:.15},
  ];
  if(e.ribbon!==null) events.push({id:'ribbon',frame:e.ribbon,path:'audio/motion/unfold.wav',durationInFrames:18,gain:.14});
  const heading = f<e.days ? (study?(episode.id==='motion-study-15' && f<episode.captions[1].from?'Üç sıfır.\nNe kadar zaman?':'Bir milyon saniye.'):f>=e.clock?'Her tur,\nbir dakika.':'Üç sıfır.\nNe kadar zaman?') : f<e.pack ? 'Saniyeler\ngüne dönüşür.' : f<e.zoom ? '11,6 gün.\nTek bir blok.' : f<e.years ? 'Aynı zaman.\nÇok daha fazlası.' : f<e.result ? 'Bir milyar saniye.\n≈ 31,7 yıl.' : '11,6 gün.\n31,7 yıl.';
  return <EpisodeComposition episode={episode} debug={debug}>
    <EventSoundTrack events={events}/>
    <div data-safe="heading" style={{...labelStyle,top:288,fontSize:study?80:88,lineHeight:1.08,fontWeight:500,whiteSpace:'pre-line'}}>{heading}</div>
    <svg width="1080" height="1920" viewBox="0 0 1080 1920" style={{position:'absolute',inset:0}}>
      <defs><clipPath id="geometry-window"><rect x="50" y="550" width="920" height={field?760:850} /></clipPath></defs>
      <g clipPath="url(#geometry-window)">
        {!field && <g>
          {/* Minute hand and second hand agree: one fast revolution = one schematic minute. */}
          <g opacity={1-dayP} transform={`translate(504 940) scale(${lerp(1.2,1,progress(f,0,90))*lerp(1,.72,dayP)})`}>
            <circle r="320" stroke={colors.guideLine} strokeWidth="3" fill="none"/>
            {Array.from({length:60},(_,i)=>{const a=i*Math.PI/30;return <path key={i} d={`M${Math.sin(a)*294} ${-Math.cos(a)*294}L${Math.sin(a)*(i%5===0?265:282)} ${-Math.cos(a)*(i%5===0?265:282)}`} stroke={i%5===0?colors.foreground:colors.guideLine} strokeWidth={i%5===0?4:2}/>;})}
            <path d="M0 45V-250" stroke={colors.accent} strokeWidth="7" transform={`rotate(${(f%90)*4})`}/>
            <path d="M0 0V-180" stroke={colors.foreground} strokeWidth="12" strokeLinecap="round" transform={`rotate(${f/15})`}/>
            <circle r="12" fill={colors.accent}/>
          </g>
          {/* Clock ticks expand into 11 whole day strips and 0.574 of the twelfth. */}
          {Array.from({length:12},(_,i)=>{
            const p=progress(f,e.days+i*(study?1:8),study?20:38);
            const angle=i*Math.PI/6;
            return <rect key={i} x={lerp(504+Math.sin(angle)*294,140+(i%3)*254,p)} y={lerp(940-Math.cos(angle)*294,650+Math.floor(i/3)*142,p)} width={lerp(4,226*Math.min(1,days-i),p)} height={lerp(15,112,p)} rx={lerp(1,3,p)} fill={colors.accent} opacity={dayP}/>;
          })}
        </g>}
        {field && <>
          <g opacity={1-ribbonP}><CameraRig camera={camera} center={[504,930]}>
            <QuantityField count={1000} columns={25} pitch={24} size={20} frame={f} from={e.zoom} duration={study?45:90} regroup={groupP} groupShape={[5,20]} leadOpacity={packP}/>
          </CameraRig></g>
          {ribbonP>0 && <TimeRibbon camera={camera} amount={ribbonP} group={groupP}/>}
          {/* A bracket denotes the original cell; it is never enlarged inside the count field. */}
          {zoomP>.98 && ribbonP===0 && <g opacity={progress(f,e.zoom+(study?60:110),20)} stroke={colors.accent} fill="none" strokeWidth="2">
            <path d={`M${504-camera.x*.76-12} ${930-camera.y*.76-10}h38v34h-38z`}/>
            <path d={`M${504-camera.x*.76-12} ${930-camera.y*.76+7}H142`}/>
          </g>}
          {/* Folded day strips merge into exactly the first equal-sized cell. */}
          {packP<1 && <g opacity={1-packP}>{Array.from({length:12},(_,i)=><rect key={i} x={lerp(140+i%3*254,504-camera.x*camera.scale,packP)} y={lerp(650+Math.floor(i/3)*142,930-camera.y*camera.scale,packP)} width={lerp(226*Math.min(1,days-i),20*camera.scale,packP)} height={lerp(112,20*camera.scale,packP)} fill={colors.accent}/>)}</g>}
          {zoomP>.98 && ribbonP===0 && <>
            <text data-safe="first-unit" x="114" y="585" fill={colors.accent} fontSize="36" fontFamily={typography.mono}>1</text>

          </>}
        </>}
      </g>
      {field && groupP>.9 && ribbonP===0 && <text data-safe="group-count" x="744" y="520" fill={colors.secondaryAccent} fontSize="36" fontFamily={typography.mono}>10 × 100</text>}
    </svg>
    {!field && <>
      <div data-safe="measure" style={{...labelStyle,top:dayP>.5?1230:1268,fontFamily:typography.mono,lineHeight:1.1,fontSize:dayP>.5?104:64,color:colors.accent}}>{dayP>.5?'≈ 11,6 gün':'1.000.000 s'}</div>
      <div data-safe="encoding" style={{...labelStyle,top:dayP>.5?1364:1370,fontSize:36,color:colors.mutedText}}>{dayP>.5?'11 tam gün + günün %57,4’ü':'Hızlandırılmış saat · 1 tur = 1 dakika'}</div>
    </>}
    {field && <>
      <div data-safe="measure" style={{...labelStyle,top:1318,fontFamily:typography.mono,lineHeight:1.1,fontSize:resultP>.5?72:42,color:colors.secondaryAccent}}>{f<e.zoom?'1 blok = 1 milyon saniye':resultP>.5?'Tam 1.000 kat.':zoomP>.98?'1 milyar saniye':'1 milyar saniyeye açılıyoruz'}</div>
      <div data-safe="encoding" style={{...labelStyle,top:1410,fontSize:34,color:colors.mutedText}}>{ribbonP>.99?'Katlanmış doğrusal zaman · 1 aralık = 1 yıl':ribbonP>0?'Aynı birimler zaman ekseninde birleşiyor':resultP>.5?'Eşit blok adedi · her blok 1 milyon saniye':'Her blok 1 milyon saniye · şematik gruplama'}</div>
    </>}
    {!hideCaptions && <CaptionTrack cues={episode.captions}/>}
  </EpisodeComposition>;
};
