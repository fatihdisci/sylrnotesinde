import {AbsoluteFill,Html5Audio,Sequence,staticFile,useCurrentFrame} from 'remotion';
import {Outro} from '../../brand/Outro';
import {typography} from '../../brand/tokens';
import {LayoutProbe} from '../../components/LayoutProbe';
import type {Episode} from '../types';
import {anchor,phase} from './choreography';
import {Sculpture} from './Sculpture';
import manifest from '../../../public/episodes/seconds-sculpture/narration-manifest.json';
const ink='#F2F0E9',coral='#F07857';
/** Isolated creative candidate. No change to the protected brand composition or captions. */
export const SculptureFrame=({episode,f,hideCaptions=false,debug=false}:{episode:Episode;f:number;hideCaptions?:boolean;debug?:boolean})=>{
 const a=(id:string)=>anchor(episode,id);const cue=episode.captions.find(c=>f>=c.from&&f<c.to);
 let title='',label='',size=118;
 if(f<a('shock')){title='MİLYON';label='BİRİM: SANİYE';size=142;}
 else if(f<a('zeros')){title='MİLYAR';label='AYNI SANİYE. BAŞKA BİR ÖLÇEK.';size=142;}
 else if(f<a('dive')){title='000';label='SADECE ÜÇ SIFIR';size=240;}
 else if(f<a('clock')){title='Zamanın\niçine bak.';size=94;}
 else if(f<a('unwind')){label='HIZLANDIRILMIŞ • 1 TUR = 1 DAKİKA';}
 else if(f<a('million')){label='DAKİKA → SAAT → GÜN';}
 else if(f<a('fraction')){title='1.000.000';label='SANİYE';size=117;}
 else if(f<a('collect')){title='11,6';label='GÜN • YAKLAŞIK';size=210;}
 else if(f<a('block')){label='ZAMAN TEK BİR PARÇAYA KATLANIYOR';}
 else if(f<a('launch')){title='Bir parça.';label='1.000.000 SANİYE';size=100;}
 else if(f<a('sample')){label='ÖLÇEK AÇILIYOR';}
 else if(f<a('thousand')){title='Her biri\n1 milyon.';size=94;}
 else if(f<a('years')){title='1.000';label='EŞİT PARÇA';size=200;}
 else if(f<a('compare')){title='31,7';label='YIL • YAKLAŞIK';size=210;}
 else if(f<a('result')){title='11,6 gün.\n31,7 yıl.';size=92;}
 else {title='1.000×';label='TAM OLARAK';size=175;}
 const textFrom=episode.direction!.events.filter(e=>e.from<=f).at(-1)!.from;
 const enter=phase(f,textFrom,textFrom+14);
 return <AbsoluteFill style={{fontFamily:typography.sans,color:ink,background:'#10191b',overflow:'hidden'}}>
  <Sculpture f={f} episode={episode}/>
  <AbsoluteFill style={{background:'linear-gradient(180deg,rgba(10,18,20,.2),transparent 36%,transparent 65%,rgba(10,18,20,.94) 87%)',pointerEvents:'none'}}/>
  <div data-safe="candidate-name" style={{position:'absolute',left:80,top:186,fontSize:22,letterSpacing:4,opacity:.72}}>SAYILARIN ÖTESİNDE <span style={{color:coral}}> / 01</span></div>
  {(title||label)&&<div data-safe="candidate-title" style={{position:'absolute',left:80,top:272,right:148,transform:`translateY(${(1-enter)*16}px)`,opacity:.6+.4*enter}}>
   {label&&<div style={{fontFamily:typography.mono,fontSize:22,letterSpacing:2,color:coral,marginBottom:18}}>{label}</div>}
   {title&&<div style={{fontSize:size,lineHeight:.94,fontWeight:600,letterSpacing:-size*.055,whiteSpace:'pre-line'}}>{title}</div>}
  </div>}
  {!hideCaptions&&cue&&<div data-safe="caption" style={{position:'absolute',left:80,right:148,top:1470,fontSize:44,lineHeight:1.28,fontWeight:400,color:ink}}>{cue.lines.map(line=><div key={line}>{line}</div>)}</div>}
  {debug&&<LayoutProbe/>}
 </AbsoluteFill>;
};
export const SecondsSculpture=({episode,hideCaptions=false,debug=false}:{episode:Episode;hideCaptions?:boolean;debug?:boolean})=>{
 const f=useCurrentFrame(),outro=episode.durationInFrames-45;
 return <AbsoluteFill>
  <Sequence durationInFrames={outro}><SculptureFrame episode={episode} f={f} hideCaptions={hideCaptions} debug={debug}/><Html5Audio src={staticFile(episode.narration[0].path)} volume={.9}/>{episode.audio.sfxPath&&<Html5Audio src={staticFile(episode.audio.sfxPath)} volume={.6}/>}</Sequence>
  <Sequence from={outro} durationInFrames={45}><Outro/>{debug&&<LayoutProbe/>}</Sequence>
 </AbsoluteFill>;
};
export const prototypeStart=anchor(manifest as Episode,'launch')-22;
export const prototypeFrames=420;
export const SculpturePrototype=()=>{
 const f=useCurrentFrame(),e=manifest as Episode;
 return <AbsoluteFill><SculptureFrame episode={e} f={f+prototypeStart}/><Html5Audio src={staticFile(e.narration[0].path)} trimBefore={prototypeStart} trimAfter={prototypeStart+prototypeFrames} volume={.9}/>{e.audio.sfxPath&&<Html5Audio src={staticFile(e.audio.sfxPath)} trimBefore={prototypeStart} trimAfter={prototypeStart+prototypeFrames} volume={.6}/>}</AbsoluteFill>;
};
