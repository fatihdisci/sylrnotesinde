import {useEffect, useState} from 'react';
import {cancelRender, continueRender, delayRender, useCurrentFrame} from 'remotion';
import {fontsReady, fontFiles} from '../brand/fonts';
import {safeArea, video} from '../brand/tokens';
/** Diagnostic only. Never mounted by final compositions. */
export const LayoutProbe = () => {
  const frame = useCurrentFrame();
  const [handle] = useState(() => delayRender('Font and safe area audit'));
  useEffect(() => {
    void fontsReady.then(() => {
      const rects = Array.from(document.querySelectorAll<HTMLElement>('[data-safe]')).map(e => {
        const r = e.getBoundingClientRect();
        return {name: e.dataset.safe, x: r.x, y: r.y, width: r.width, height: r.height,
          right: r.right, bottom: r.bottom, overflow: e.scrollWidth > e.clientWidth + 1};
      });
      const violations = rects.filter(r => r.x < safeArea.left - 1 || r.y < safeArea.top - 1 ||
        r.right > video.width - safeArea.right + 1 || r.bottom > video.height - safeArea.bottom + 1 || r.overflow);
      const collisions = rects.flatMap((a, i) => rects.slice(i + 1).filter(b =>
        a.x < b.right && a.right > b.x && a.y < b.bottom && a.bottom > b.y).map(b => [a.name, b.name]));
      const fonts = fontFiles.map(f => ({...f, loaded: document.fonts.check(`${f.weight} 44px "${f.family}"`, 'Öö Üü İı Şş Ğğ Çç 1.000.000 11,6')}));
      console.info(`LAYOUT_AUDIT:${JSON.stringify({frame, rects, violations, collisions, fonts})}`);
      continueRender(handle);
    }).catch(cancelRender);
  }, [frame, handle]);
  return null;
};
