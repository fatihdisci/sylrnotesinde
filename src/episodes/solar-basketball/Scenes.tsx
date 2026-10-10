import {AbsoluteFill,Html5Audio,Sequence,staticFile,useCurrentFrame} from 'remotion';
import * as THREE from 'three';
import {Outro} from '../../brand/Outro';
import {BrandSignature} from '../../brand/BrandSignature';
import {colors,typography} from '../../brand/tokens';
import {LayoutProbe} from '../../components/LayoutProbe';
import type {Episode} from '../types';
import {SolarWorld} from './World';
import {anchor,cameraPose,phase} from './camera';
import {positions} from './model';
const ink=colors.foreground;
const WideMarkers=({f,episode}:{f:number;episode:Episode})=>{
 const pose=cameraPose(f,episode);const camera=new THREE.PerspectiveCamera(pose.fov,1080/1920,.00001,2800);camera.position.set(...pose.eye);camera.lookAt(...pose.target);camera.updateMatrixWorld();
 const labels=[{key:'sun',text:'Güneş',dx:-175,dy:32},{key:'earth',text:'Dünya',dx:175,dy:-24},{key:'jupiter',text:'Jüpiter',dx:-175,dy:-18},{key:'neptune',text:'Neptün',dx:145,dy:32}] as const;
 return <svg width={1080} height={1920} style={{position:'absolute',inset:0,pointerEvents:'none',opacity:phase(f,anchor(episode,'whole')-20,anchor(episode,'whole')+24)}}>
  {labels.map(l=>{const p=new THREE.Vector3(...positions[l.key]).project(camera),x=(p.x+1)*540,y=(1-p.y)*960;
   const tx=Math.max(180,Math.min(820,x+l.dx)),ty=Math.max(620,Math.min(1325,y+l.dy));
   return <g key={l.key}><circle cx={x} cy={y} r={5} fill={l.key==='sun'?colors.accent:colors.secondaryAccent}/><path d={`M${x},${y} L${tx},${ty-10}`} stroke={colors.mutedText} strokeWidth={1.5} fill="none"/><text data-safe={`marker-${l.key}`} x={tx} y={ty} fill={ink} fontSize={34} fontFamily={typography.sans} textAnchor="middle">{l.text}</text></g>;
  })}
 </svg>;
};
const ModelMarkers=({f,episode}:{f:number;episode:Episode})=>{
 const a=(id:string)=>anchor(episode,id),pose=cameraPose(f,episode);
 const camera=new THREE.PerspectiveCamera(pose.fov,1080/1920,.00001,4000);camera.position.set(...pose.eye);camera.lookAt(...pose.target);camera.updateMatrixWorld();
 const project=(key:keyof typeof positions)=>{const p=new THREE.Vector3(...positions[key]).project(camera);return {x:(p.x+1)*540,y:(1-p.y)*960,z:p.z};};
 if(f>=a('moon-range')+25&&f<a('moon-size')){
  const earth=project('earth'),moon=project('moon');
  return <svg width={1080} height={1920} style={{position:'absolute',inset:0,pointerEvents:'none'}}>
   <path d={`M${earth.x},1140 v24 M${earth.x},1152 H${moon.x} M${moon.x},1140 v24`} stroke={colors.secondaryAccent} strokeWidth={2} fill="none"/>
   <text data-safe="earth-label" x={earth.x} y={1082} fill={ink} fontSize={36} fontFamily={typography.sans} textAnchor="middle">Dünya</text>
   <text data-safe="moon-label" x={moon.x} y={1082} fill={ink} fontSize={36} fontFamily={typography.sans} textAnchor="middle">Ay</text>
  </svg>;
 }
 const key=f>=a('street')&&f<a('arrival')?'earth':f>=a('jup-road')&&f<a('neptune')?'jupiter':null;
 if(!key)return null;
 const p=project(key);if(p.z<0||p.z>1||p.x<80||p.x>932||p.y<650||p.y>1250)return null;
 return <svg width={1080} height={1920} style={{position:'absolute',inset:0,pointerEvents:'none'}}>
  <circle cx={p.x} cy={p.y} r={6} fill={colors.secondaryAccent}/>
  <path d={`M${p.x},${p.y} l86,-42 h90`} stroke={colors.secondaryAccent} strokeWidth={1.5} fill="none"/>
  <text data-safe="destination-marker" x={p.x+92} y={p.y-58} fill={ink} fontSize={34} fontFamily={typography.sans}>{key==='earth'?'Dünya':'Jüpiter'}</text>
  <text x={p.x+92} y={p.y-12} fill={colors.mutedText} fontSize={23} fontFamily={typography.mono}>konum işareti</text>
 </svg>;
};
export const SolarFrame=({f,episode,hideCaptions=false,debug=false}:{f:number;episode:Episode;hideCaptions?:boolean;debug?:boolean})=>{
 const a=(id:string)=>anchor(episode,id),cue=episode.captions.find(c=>f>=c.from&&f<c.to);
 let title='',measure='',eyebrow='';
 if(f<a('ball-size')){title='Güneş, bir\nbasketbol topu.';eyebrow='ÖLÇEĞİ DEĞİŞTİR';}
 else if(f<a('earth-size')){measure='24 cm';eyebrow='GÜNEŞİN MODEL ÇAPI';}
 else if(f<a('distance-shock')){measure='2,2 mm';eyebrow='DÜNYANIN MODEL ÇAPI';}
 else if(f<a('street')){title='Asıl fark,\naradaki boşluk.';eyebrow='BOYUTTAN UZAKLIĞA';}
 else if(f<a('arrival')){measure='25,8 m';eyebrow='GÜNEŞ → DÜNYA';}
 else if(f<a('moon')){title='Sokağın\nkarşısında.';eyebrow='AYNI ODAYA SIĞMIYOR';}
 else if(f<a('moon-size')){measure='6,6 cm';eyebrow='DÜNYA → AY';}
 else if(f<a('jupiter')){measure='0,6 mm';eyebrow='AYIN MODEL ÇAPI';}
 else if(f<a('jup-road')){measure='2,5 cm';eyebrow='JÜPİTERİN MODEL ÇAPI';}
 else if(f<a('neptune')){measure='134,3 m';eyebrow='GÜNEŞ → JÜPİTER';}
 else if(f<a('far-flight')){title='Sırada\nNeptün var.';eyebrow='EN UZAK GEZEGEN';}
 else if(f<a('neighborhood')){measure='778,8 m';eyebrow='GÜNEŞ → NEPTÜN';}
 else if(f<a('quiet')){title='Bir top.\nKoca bir mahalle.';eyebrow='AYNI MATEMATİKSEL ÖLÇEK';}
 else {title=f<a('final')?'Uzay gerçekten\nbüyük değil.':'Aklın alıştığından\nçok daha büyük.';}
 const latest=episode.direction!.events.filter(e=>e.from<=f).at(-1)!;
 const enter=phase(f,latest.from,latest.from+10);
 return <AbsoluteFill style={{fontFamily:typography.sans,color:ink,background:'#0c151c',overflow:'hidden'}}>
  <SolarWorld f={f} episode={episode}/>
  <AbsoluteFill style={{pointerEvents:'none',background:'linear-gradient(180deg,rgba(12,21,28,.18) 0%,transparent 38%,transparent 67%,rgba(12,21,28,.95) 81%)'}}/>
  <BrandSignature/>
  <div data-safe="solar-title" style={{position:'absolute',left:80,right:148,top:275,opacity:.78+.22*enter,transform:`translateY(${(1-enter)*10}px)`}}>
   {eyebrow&&<div style={{fontFamily:typography.mono,color:colors.accent,fontSize:25,letterSpacing:2,marginBottom:16}}>{eyebrow}</div>}
   {title&&<div style={{fontSize:86,lineHeight:1.04,fontWeight:500,letterSpacing:-3.5,whiteSpace:'pre-line'}}>{title}</div>}
   {measure&&<div style={{fontFamily:typography.mono,fontSize:124,letterSpacing:-7,lineHeight:1.05}}>{measure}</div>}
  </div>
  <ModelMarkers f={f} episode={episode}/>
  {f>=a('whole')-20&&<WideMarkers f={f} episode={episode}/>}
  {!hideCaptions&&cue&&<div data-safe="caption" style={{position:'absolute',left:80,right:148,top:1478,fontSize:44,lineHeight:1.28,fontWeight:400,textShadow:'0 2px 6px #0c151c'}}>{cue.lines.map(line=><div key={line}>{line}</div>)}</div>}
  {debug&&<LayoutProbe/>}
 </AbsoluteFill>;
};
/** Episode-specific art direction, canonical fonts, signature and untouched 45f outro. */
export const SolarBasketball=({episode,hideCaptions=false,debug=false}:{episode:Episode;hideCaptions?:boolean;debug?:boolean})=>{
 const f=useCurrentFrame(),outro=episode.durationInFrames-45;
 return <AbsoluteFill>
  <Sequence durationInFrames={outro}>
   <SolarFrame f={f} episode={episode} hideCaptions={hideCaptions} debug={debug}/>
   <Html5Audio src={staticFile(episode.narration[0].path)} volume={.9}/>
   {episode.audio.sfxPath&&<Html5Audio src={staticFile(episode.audio.sfxPath)} volume={.6}/>}
   {episode.audio.musicPath&&<Html5Audio src={staticFile(episode.audio.musicPath)} volume={.12}/>}
  </Sequence>
  <Sequence from={outro} durationInFrames={45}><Outro/>{debug&&<LayoutProbe/>}</Sequence>
 </AbsoluteFill>;
};
