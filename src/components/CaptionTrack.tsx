import {useCurrentFrame} from 'remotion';
import {colors, safeArea, typography, video} from '../brand/tokens';
import {motion, progress} from '../brand/motion';
export type CaptionCue = {from: number; to: number; lines: readonly string[]};
export const CaptionTrack = ({cues}: {cues: readonly CaptionCue[]}) => {
  const frame = useCurrentFrame();
  const cue = cues.find(c => frame >= c.from && frame < c.to);
  if (!cue) return null;
  if (cue.lines.length > 2) throw new Error('Captions must have at most two lines');
  return <div data-safe="caption" style={{position: 'absolute', left: safeArea.left, right: safeArea.right,
    top: video.height - safeArea.bottom - 138, fontSize: typography.caption, lineHeight: 1.32, fontWeight: 400,
    color: colors.foreground, opacity: progress(frame, cue.from, motion.label)}}>
    {cue.lines.map(line => <div key={line}>{line}</div>)}
  </div>;
};
