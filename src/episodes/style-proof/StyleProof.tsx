import {useCurrentFrame} from 'remotion';
import {motion, progress} from '../../brand/motion';
import {colors, safeArea, typography} from '../../brand/tokens';
import {CaptionTrack} from '../../components/CaptionTrack';
import {ComparisonScene} from '../../components/ComparisonScene';
import {EpisodeComposition} from '../../components/EpisodeComposition';
import {MeasurementLine} from '../../components/MeasurementLine';
import {NumberDisplay} from '../../components/NumberDisplay';
import {ScaleStage, stage, toScreen} from '../../components/ScaleStage';
import {styleProofEpisode} from './episode';
import {proofState, units} from './model';

const ProofScene = () => {
  const f = useCurrentFrame();
  const {count, camera} = proofState(f);
  const edgeLeft = toScreen(0, 0, camera).x;
  const edgeRight = toScreen(f < 210 ? 135 : 771, 0, camera).x;
  const line = progress(f, f < 90 ? 0 : f < 210 ? 90 : 210, motion.measurement);
  return <>
    <h1 data-safe="hook" style={{position: 'absolute', margin: 0, left: safeArea.left, top: 292, width: stage.width,
      fontSize: typography.title, fontWeight: 500, lineHeight: 1.12, letterSpacing: -2.6}}>
      Bir sıfır,<br />ölçeği değiştirir.
    </h1>
    <div data-safe="count" style={{position: 'absolute', left: safeArea.left, top: 536, display: 'flex', alignItems: 'baseline', gap: 28}}>
      <NumberDisplay value={count} /><span style={{fontSize: 36, color: colors.mutedText}}>birim</span>
    </div>
    <ComparisonScene encoding="1 kare = 1 birim">
      <ScaleStage camera={camera}>
        {units.slice(0, count).map(u => <rect key={u.id} x={u.x} y={u.y}
          width={u.id < 10 && f < 24 ? 14 - 5 * progress(f, 0, 24) : u.size} height={u.size}
          fill={u.id < 10 ? colors.accent : u.id < 100 ? colors.secondaryAccent : colors.foreground}
          opacity={f < 12 ? 0.65 + 0.35 * progress(f, 0, motion.label) : 1} />)}
      </ScaleStage>
    </ComparisonScene>
    <svg style={{position: 'absolute', left: stage.x, top: 1408}} width={stage.width} height={34}>
      <MeasurementLine x1={Math.max(0, edgeLeft)} x2={Math.min(stage.width, edgeRight)} y={16} progress={line} />
    </svg>
    <CaptionTrack cues={styleProofEpisode.captions} />
  </>;
};
export const StyleProof = () => <EpisodeComposition episode={styleProofEpisode}><ProofScene /></EpisodeComposition>;
export const StyleProofDebug = () => <EpisodeComposition episode={styleProofEpisode} debug><ProofScene /></EpisodeComposition>;
