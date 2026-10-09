# Teknik kaynaklar ve kilitli sürümler

Doğrulama tarihi:9 Ekim2026. Resmî dokümantasyon + npm registry metadata birlikte kontrol edildi.

- [Remotion React19 uyumluluğu](https://www.remotion.dev/docs/react-19): Remotion4 destekler. React/ReactDOM19.3.0 ve @types19.3.0 kuruldu.
- [Remotion font paketi](https://www.remotion.dev/docs/fonts-api/): tüm Remotion/@remotion paketlerinin aynı sürüme, caret olmadan sabitlenmesi. Kurulan sürüm4.0.534; npm registry aynı sürümü bildirdi.
- [Yerel font yükleme](https://www.remotion.dev/docs/fonts-api/load-font): staticFile ile yerel yükleme ve render bekletme.
- [Yerel browser hazırlığı](https://www.remotion.dev/docs/renderer/ensure-browser): Chromium ilk hazırlık sırasında indirilir. Bu kurulumun Chrome Headless Shell sürümü157.0.8080.0, mac-arm64.
- [Programatik MP4 render](https://www.remotion.dev/docs/renderer/render-media): bundle/selectComposition/renderMedia yerel üretim hattı.
- [IBM resmî Plex kaynağı](https://github.com/IBM/plex): IBM yayımlayıcısının @ibm/plex-sans1.1.0 ve @ibm/plex-mono2.5.0 paketleri. Tam WOFF2 dosyaları. [OFL lisansı](https://github.com/IBM/plex/blob/master/LICENSE.txt) `public/fonts/` altında saklandı.

Node22.22.3, npm10.9.8, TypeScript5.9.3. ESLint10.12.0 + typescript-eslint8.71.1 kullanıldı; registry peer metadata ESLint10 ve TS<6.1 desteğini doğruladı. İlk kurulumda gelen ESLint9 deprecated bildirimi nedeniyle desteklenen10 sürümüne geçildi. Doğrudan tüm npm bağımlılıkları exact; transitif sürümler ve integrity değerleri package-lock.json içinde. Python QA bağımlılıkları requirements-qa.txt içinde exact.

Araştırma okumaları agent-reach web/Jina yolu ve resmî web sayfalarıyla yapıldı. Araştırma render sürecinden bağımsızdır. Üretim sırasında dış font/ses servisi kullanılmaz.
