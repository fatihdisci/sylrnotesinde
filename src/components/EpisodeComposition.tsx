import type {ReactNode} from 'react';
import {AbsoluteFill, Html5Audio, Sequence, staticFile} from 'remotion';
import {Outro} from '../brand/Outro';
import {BrandSignature} from '../brand/BrandSignature';
import {colors, outroSpec, typography} from '../brand/tokens';
import {SafeAreaDebug} from './SafeAreaDebug';
import {LayoutProbe} from './LayoutProbe';
import {validateEpisode, type Episode} from '../episodes/types';
/** Central composition envelope: episode code supplies scenes, not brand overrides. */
export const EpisodeComposition = ({episode, children, debug = false}: {
  episode: Episode; children: ReactNode; debug?: boolean;
}) => {
  validateEpisode(episode);
  const contentFrames = episode.durationInFrames - outroSpec.frames;
  return <AbsoluteFill style={{backgroundColor: colors.background, color: colors.foreground, fontFamily: typography.sans}}>
    <Sequence durationInFrames={contentFrames}>
      <BrandSignature />
      {children}
      {episode.narration.map(n => <Sequence key={n.id} from={n.from} durationInFrames={n.durationInFrames} layout="none">
        <Html5Audio src={staticFile(n.path)} volume={0.9} />
      </Sequence>)}
      {episode.audio.sfxPath && <Html5Audio src={staticFile(episode.audio.sfxPath)} volume={0.6} />}
      {episode.audio.musicPath && <Html5Audio src={staticFile(episode.audio.musicPath)} volume={0.12} />}
    </Sequence>
    <Sequence from={contentFrames} durationInFrames={outroSpec.frames}><Outro /></Sequence>
    {debug && <><SafeAreaDebug /><LayoutProbe /></>}
  </AbsoluteFill>;
};
