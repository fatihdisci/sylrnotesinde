# Sayıların Ötesinde

Yerelde çalışan **Remotion + React + TypeScript motion graphics projesi**. SVG geometri, bölüm başına özgün TSX sahneler ve ortak marka sistemi. Sürüm: **0.1-candidate**, kullanıcı tarafından henüz onaylanmadı.

## Çıktılar

- `renders/style-proof.mp4`: 15 s / 450 kare / 1080×1920 / 30 FPS, geçici Türkçe anlatım + özgün efektler.
- `renders/outro.mp4`: 1,5 s / 45 kare, sabit kapanış.
- `renders/style-board.png`: renk, tipografi ve yerleşim panosu.
- `renders/qa/contact-sheet.png` ve `frame-*.png`: gerçek MP4 inceleme kareleri.
- `QA.md`: doğrulananlar, düzeltilenler ve inceleme sınırları.

## Çalıştırma

Mac üzerinde Node **22.22.3** / npm **10.9.8** ile doğrulandı. Node 22.22.3 veya uyumlu 22.x kullan. FFmpeg ve ffprobe PATH içinde olmalı; QA için Python 3.14 ve aşağıdaki kilitli paketler kullanıldı.

```sh
npm ci
npm run browser:prepare
npm run preview
```

Önizleme: http://localhost:3020/StyleProof — `StyleProof`, `Outro`, `StyleBoard`, `StyleProofDebug` kompozisyonları kayıtlı. Önizleme React geliştirici sunucusudur; yayınlanacak web sitesi değildir. Chrome indirmesi yalnızca ilk hazırlık içindir. Fontlar ve tüm ses dosyaları `public/` içinde hazırdır.

```sh
npm run check
npm run render             # iki MP4 + style-board.png
npm run render:proof
npm run render:outro
npm run render:board
npm run qa:layout           # Chromium font/taşma/çakışma/güvenli alan
npm run references:check    # sabit 5 referansla piksel karşılaştırması
```

Tam medya QA:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-qa.txt
npm run qa:fonts
npm run qa:media
```

`npm run render` ses üretmez, font indirmez ve dış servis çağırmaz. İlk `npm ci` ve `browser:prepare` sonrasında render tamamen yereldir. Kaynak varlıklar silinirse `npm run assets:fonts`, `npm run assets:sound`, `npm run assets:voice` ile ayrı hazırlık yapılır. Ses üretimi normal render akışına bağlı değildir. `assets:voice`, Mac'in yerel Yelda sesini ve FFmpeg'i kullanır; yeni bir üretimden sonra süreleri yeniden doğrula.

## Yeni bölüm

Önce AGENTS.md ve orada listelenen dört belgeyi oku. `src/episodes/<id>/episode.ts` içinde `Episode` türüne uygun senaryo, kaynaklar, süreler ve ses yollarını tanımla; `Scenes.tsx` içinde konuya özel animasyonları yaz. Yerel varlıkları `public/episodes/<id>/` altına koy. Sahneyi `EpisodeComposition` ile sar ve `src/compositions/Root.tsx` içine 1080×1920, 30 FPS, outro dahil 1200–1350 karelik `Composition` ekle. Render: `npx remotion render src/index.ts <CompositionId> renders/<id>.mp4`.

Ortak bileşenler `src/components/`, marka `src/brand/`, üretim araçları `scripts/` altında. Her sahne aynı şablonu doldurmak zorunda değil. Three.js, veritabanı, bulut servis veya yönetim paneli kullanılmıyor.

Yerel anlatım **geçici**. Sözcük zamanları doğrulanmadı; altyazılar sahne/cümle öbekleriyle ilerliyor. Sağlayıcı/kimlik/ayarlar `src/episodes/narrator.config.ts` içinde; anahtar yalnızca ortam değişkeninden alınmalı.

Font kaynağı/lisansı: `public/fonts/SOURCE.md` ve yanındaki OFL dosyaları. Teknik kaynaklar/sürüm doğrulaması: `docs/TECHNICAL_SOURCES.md`.
