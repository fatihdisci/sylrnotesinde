import {useCurrentFrame} from 'remotion';
import type {Episode} from '../types';
import {colors, typography} from '../../brand/tokens';
import {progress} from '../../brand/motion';
import {CaptionTrack} from '../../components/CaptionTrack';
import {EpisodeComposition} from '../../components/EpisodeComposition';
import {SceneSpace} from '../../components/SceneSpace';

export const ProductionCheck = ({episode, hideCaptions = false, debug = false}: {episode: Episode; hideCaptions?: boolean; debug?: boolean}) => {
  const f = useCurrentFrame();
  const at = (i: number) => episode.captions[i].from;
  const p = progress(f, at(7), 54);
  // True linear length ratio: the short unit is840 world units, long is840,000.
  // Camera zooms out1000×. All readable labels remain in the screen layer.
  const zoom = Math.exp(-Math.log(1000) * p);
  const units = Math.round(1000 * progress(f, at(9), 60));
  const result = f >= at(12);
  const number = f < at(3) ? '1.000 ×' : f < at(5) ? '11,6' : f < at(7) ? '31,7' : result ? '1 km' : '1 : 1.000';
  const unit = f < at(3) ? 'milyon → milyar' : f < at(5) ? 'gün' : f < at(7) ? 'yıl' : result ? '= 1.000 m' : 'doğrusal uzunluk oranı';
  return <EpisodeComposition episode={episode} debug={debug}>
    <div data-safe="heading" style={{position: 'absolute', left: 72, top: 300, fontSize: 88, lineHeight: 1.12, fontWeight: 500}}>Saniyelerin<br />ölçeği.</div>
    <div data-safe="number" style={{position: 'absolute', left: 72, top: 535, fontSize: 142, fontFamily: typography.mono, color: colors.foreground}}>{number}</div>
    <div data-safe="unit" style={{position: 'absolute', left: 76, top: 724, fontSize: 38, color: colors.secondaryAccent}}>{unit}</div>
    <SceneSpace mode={result ? 'object' : p ? 'journey' : 'comparison'} style={{top: 850, height: 420}}>
      <svg width="864" height="420" viewBox="0 0 864 420" style={{overflow: 'hidden'}}>
        <path d="M12 24V384 M852 24V384" stroke={colors.guideLine} strokeWidth={2} />
        <g transform={`translate(12 0) scale(${zoom} 1)`}>
          <path d={`M0 90H${840 * progress(f, 0, 24)}`} stroke={colors.accent} strokeWidth={8} />
          <path d={`M0 220H${840000 * progress(f, at(5), 40)}`} stroke={colors.secondaryAccent} strokeWidth={8} />
          {f >= at(9) && <path d={`M0 90H${840 * units}`} stroke={colors.accent} strokeWidth={8} />}
          {Array.from({length: 1001}, (_, i) => <path key={i} d={`M${i*840} 211V229`} stroke={colors.background} strokeWidth={0.15} vectorEffect="non-scaling-stroke" />)}
        </g>
        {result && <><path d="M12 345H852" stroke={colors.foreground} strokeWidth={3}/>{Array.from({length: 11}, (_, i) => <path key={i} d={`M${12+i*84} 333V357`} stroke={colors.foreground} strokeWidth={3}/>)}</>}
      </svg>
    </SceneSpace>
    <div data-safe="encoding" style={{position: 'absolute', left: 72, top: 1300, width: 864, fontSize: 36, color: colors.mutedText}}>{result ? 'Aynı mesafe · farklı birim' : p > .99 ? 'Her parça = 1 milyon saniye' : f >= at(5) ? 'Uzun çizgi kadrajın dışında →' : 'Uzunluk süreyle doğru orantılı.'}</div>
    {!hideCaptions && <CaptionTrack cues={episode.captions} />}
  </EpisodeComposition>;
};
