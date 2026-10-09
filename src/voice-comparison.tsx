import {Composition, registerRoot} from 'remotion';
import {VoiceComparisonReel, type VoiceReelProps} from './compositions/VoiceComparisonReel';
import {video} from './brand/tokens';
const defaults: VoiceReelProps = {text: '', clips: [], fps: 30, durationInFrames: 45};
const Root = () => <Composition id="VoiceComparisonReel" component={VoiceComparisonReel}
  width={video.width} height={video.height} fps={video.fps} durationInFrames={45} defaultProps={defaults}
  calculateMetadata={({props}) => ({durationInFrames: props.durationInFrames})} />;
registerRoot(Root);
