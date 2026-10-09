import {AbsoluteFill, Html5Audio, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {BrandSignature} from '../brand/BrandSignature';
import {Outro} from '../brand/Outro';
import {colors, outroSpec, safeArea, typography} from '../brand/tokens';
import {progress} from '../brand/motion';
import '../brand/fonts';

export type VoiceClip = {
  model: string; name: string; voice: string; audio: string; fromFrame: number;
  durationInFrames: number; audioFrames: number; seconds: number; peaks: number[];
};
export type VoiceReelProps = {text: string; fps: number; durationInFrames: number; clips: VoiceClip[]};

const Sample = ({clip, index, total}: {clip: VoiceClip; index: number; total: number}) => {
  const frame = useCurrentFrame();
  const played = Math.max(0, Math.min(1, (frame - 6) / clip.audioFrames));
  const shown = progress(frame, 0, 12);
  const profile = clip.voice === 'default' ? 'Tek ses' : clip.voice;
  const category = clip.voice.startsWith('M') ? 'ERKEK SES' : clip.voice.startsWith('F') ? 'KADIN SES' : 'SABİT PROFİL';
  const wave = clip.peaks.map((p, i) => {
    const x = 4 + i * 5.35;
    const h = Math.max(3, Math.sqrt(p) * 126);
    return `M${x},${138 - h}v${h * 2}`;
  }).join(' ');
  return <AbsoluteFill style={{backgroundColor: colors.background, color: colors.foreground, fontFamily: typography.sans}}>
    <BrandSignature />
    <div style={{position: 'absolute', left: safeArea.left, right: safeArea.right, top: 310, display: 'flex', justifyContent: 'space-between', alignItems: 'baseline'}}>
      <span style={{fontSize: 32, color: colors.mutedText, letterSpacing: 3}}>ANLATICI KARŞILAŞTIRMASI</span>
      <span style={{fontSize: 36, color: colors.secondaryAccent, fontFamily: typography.mono}}>{String(index + 1).padStart(2, '0')} / {total}</span>
    </div>
    <div style={{position: 'absolute', left: safeArea.left, right: safeArea.right, top: 490, opacity: shown}}>
      <div style={{fontSize: 88, fontWeight: 600, lineHeight: 1.15, letterSpacing: -2}}>{clip.name}</div>
      <div style={{fontSize: 164, fontFamily: typography.mono, color: colors.accent, lineHeight: 1.25, marginTop: 30}}>{profile}</div>
      <div style={{fontSize: 34, color: colors.mutedText, letterSpacing: 4, marginTop: 10}}>{category}</div>
    </div>
    <svg style={{position: 'absolute', top: 930, left: safeArea.left}} width={864} height={276} viewBox="0 0 864 276" aria-label="Gerçek ses dalga biçimi">
      <defs><clipPath id="played"><rect x={0} y={0} width={864 * played} height={276} /></clipPath></defs>
      <path d={wave} stroke={colors.guideLine} strokeWidth={3} strokeLinecap="round" />
      <path d={wave} stroke={colors.secondaryAccent} strokeWidth={3} strokeLinecap="round" clipPath="url(#played)" />
    </svg>
    <div style={{position: 'absolute', left: safeArea.left, right: safeArea.right, top: 1280}}>
      <div style={{fontSize: 30, color: colors.mutedText, letterSpacing: 3, marginBottom: 24}}>AYNI CÜMLE · DOĞAL KONUŞMA HIZI</div>
      <div style={{fontSize: 48, lineHeight: 1.5}}>
        Küçük bir fark, ölçek değiştiğinde<br />bambaşka bir dünyaya dönüşebilir.
      </div>
    </div>
    <div style={{position: 'absolute', left: safeArea.left, right: safeArea.right, top: 1550, display: 'flex', gap: 10}}>
      {Array.from({length: total}, (_, i) => <div key={i} style={{height: 4, flex: 1, backgroundColor: i === index ? colors.accent : i < index ? colors.mutedText : colors.guideLine}} />)}
    </div>
    <div style={{position: 'absolute', left: safeArea.left, top: 1578, color: colors.mutedText, fontSize: 26}}>Yerel yapay zekâ seslendirmesi · Ses düzeyleri eşitlendi</div>
    <Sequence from={6}><Html5Audio src={staticFile(clip.audio)} /></Sequence>
  </AbsoluteFill>;
};

export const VoiceComparisonReel = ({clips}: VoiceReelProps) => {
  const end = clips.reduce((sum, clip) => sum + clip.durationInFrames, 0);
  return <AbsoluteFill style={{backgroundColor: colors.background}}>
    {clips.map((clip, index) => <Sequence key={`${clip.model}-${clip.voice}`} from={clip.fromFrame} durationInFrames={clip.durationInFrames}>
      <Sample clip={clip} index={index} total={clips.length} />
    </Sequence>)}
    <Sequence from={end} durationInFrames={outroSpec.frames}><Outro /></Sequence>
  </AbsoluteFill>;
};
