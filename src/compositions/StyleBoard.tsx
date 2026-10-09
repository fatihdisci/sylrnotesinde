import {AbsoluteFill} from 'remotion';
import {BrandMark} from '../brand/BrandMark';
import {BRAND_VERSION, colors, safeArea, typography} from '../brand/tokens';
export const StyleBoard = () => <AbsoluteFill style={{backgroundColor: colors.background, color: colors.foreground,
  padding: '180px 144px 300px 72px', fontFamily: typography.sans}}>
  <div style={{display: 'flex', alignItems: 'center', gap: 26}}><BrandMark width={111} />
    <div style={{fontSize: 30, color: colors.mutedText, letterSpacing: 2}}>GÖRSEL KİMLİK / {BRAND_VERSION}</div></div>
  <div style={{fontSize: 104, lineHeight: 1.05, fontWeight: 500, letterSpacing: -3, marginTop: 64}}>Sayıların<br />Ötesinde</div>
  <div style={{fontSize: 44, color: colors.mutedText, marginTop: 36}}>Büyüklüğü görünür kıl.</div>
  <div style={{fontFamily: typography.mono, fontSize: 136, letterSpacing: -6, marginTop: 32}}>1.000.000</div>
  <div style={{fontSize: 36, color: colors.mutedText, marginTop: 8}}>IBM Plex Mono · 400 / 500</div>
  <div style={{marginTop: 42, fontSize: 46}}>Ölçek, ölçüm, düşünce.</div>
  <div style={{fontSize: 36, color: colors.mutedText, marginTop: 12}}>IBM Plex Sans · 400 / 500 / 600</div>
  <div style={{display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '32px 24px', marginTop: 48}}>
    {Object.entries(colors).map(([name, hex]) => <div key={name}>
      <div style={{height: 65, backgroundColor: hex, border: `1px solid ${colors.guideLine}`}} />
      <div style={{fontSize: 26, marginTop: 14, color: colors.mutedText}}>{name}</div>
      <div style={{fontFamily: typography.mono, fontSize: 32, marginTop: 4}}>{hex}</div>
    </div>)}
  </div>
  <div style={{marginTop: 32, borderTop: `2px solid ${colors.guideLine}`, paddingTop: 24, fontSize: 32,
    lineHeight: 1.5, color: colors.mutedText}}>
    1080 × 1920 · 30 FPS<br />
    Yerleşim: {safeArea.left} / {safeArea.right} / {safeArea.top} / {safeArea.bottom} px<br />
    Sol / sağ / üst / alt · ayarlanabilir başlangıç payları
  </div>
</AbsoluteFill>;
