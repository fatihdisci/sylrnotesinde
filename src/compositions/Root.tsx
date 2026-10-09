import {Composition} from 'remotion';
import '../brand/fonts';
import {Outro} from '../brand/Outro';
import {outroSpec, video} from '../brand/tokens';
import {StyleProof, StyleProofDebug} from '../episodes/style-proof/StyleProof';
import {StyleBoard} from './StyleBoard';
export const Root = () => <>
  <Composition id="StyleProof" component={StyleProof} durationInFrames={450} {...video} />
  <Composition id="Outro" component={Outro} durationInFrames={outroSpec.frames} {...video} />
  <Composition id="StyleProofDebug" component={StyleProofDebug} durationInFrames={450} {...video} />
  <Composition id="StyleBoard" component={StyleBoard} durationInFrames={1} {...video} />
</>;
