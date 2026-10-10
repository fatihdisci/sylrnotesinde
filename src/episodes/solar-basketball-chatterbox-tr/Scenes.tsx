import {AbsoluteFill,Html5Audio,Sequence,staticFile,useCurrentFrame} from 'remotion';
import {Outro} from '../../brand/Outro';
import {LayoutProbe} from '../../components/LayoutProbe';
import type {Episode} from '../types';
import {SolarFrame} from '../solar-basketball/Scenes';
import mixLevels from './audio-mix.json';
/** Original authored world, independently timed and mixed for this recording. */
export const SolarBasketballChatterbox=({episode,hideCaptions=false,debug=false}:{episode:Episode;hideCaptions?:boolean;debug?:boolean})=>{
 const f=useCurrentFrame(),outro=episode.durationInFrames-45;
 return <AbsoluteFill>
  {/* Local label separation for the newly timed wide-camera transition. */}
  <style>{'[data-safe="marker-jupiter"] {transform: translateY(-18px);}'}</style>
  <Sequence durationInFrames={outro}>
   <SolarFrame f={f} episode={episode} hideCaptions={hideCaptions} debug={debug}/>
   <Html5Audio src={staticFile(episode.narration[0].path)} volume={mixLevels.narration}/>
   {episode.audio.sfxPath&&<Html5Audio src={staticFile(episode.audio.sfxPath)} volume={mixLevels.effects}/>}
   {episode.audio.musicPath&&<Html5Audio src={staticFile(episode.audio.musicPath)} volume={mixLevels.music}/>}
  </Sequence>
  <Sequence from={outro} durationInFrames={45}><Outro/>{debug&&<LayoutProbe/>}</Sequence>
 </AbsoluteFill>;
};
