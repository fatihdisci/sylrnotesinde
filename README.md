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

StyleProof’taki Yelda anlatımı **tarihsel ve geçici** olarak korunur. Yeni bölümlerin kalıcı anlatıcısı kullanıcı seçimiyle **Supertonic 3 / M1 erkek sesi** oldu. Tek ayar kaynağı `tts/config/narrator.json`; eski `src/episodes/narrator.config.ts` yalnız StyleProof/Yelda hazırlığı içindir. Sözcük zamanları doğrulanmış sayılmaz; altyazılar ayrıca gözden geçirilir.

Font kaynağı/lisansı: `public/fonts/SOURCE.md` ve yanındaki OFL dosyaları. Teknik kaynaklar/sürüm doğrulaması: `docs/TECHNICAL_SOURCES.md`.

## Yerel Türkçe TTS karşılaştırması

Kullanıcının seçtiği kalıcı anlatıcı: **Supertonic 3 / M1 erkek sesi**, doğal hız (`speed=1` → yerel 1,05), CPU, seed42. Antalia ve EMA’nın yalnız bu projedeki ortamları, ağırlıkları ve kaynak klonları kaldırıldı; karşılaştırma sesleri/video, raporlar, lisanslar ve kilitler korundu. Görsel kimlik, animasyonlar, outro ve StyleProof değişmedi. [Seçim ve temizlik kaydı](tts/docs/SELECTION.md).

```sh
npm run tts:compare           # http://127.0.0.1:3030
npm run tts:generate -- --text 'Ölçek değişir.' --output tts/outputs/manual/ornek.wav --os-offline
npm run tts:episode -- --id yeni-bolum --text-file anlatim.txt
npm run tts:test
npm run tts:qa
npm run tts:offline
```

72 ana örnek + eşitlenmiş dinleme kopyaları `tts/outputs/` altında. Kör A/B/C, on Supertonic profili, doğal hız / sayı normalizasyonu / yaklaşık 42 sn varyantları, dört ölçütte puan ve yorum, yerel JSON kayıt ve test sonu isim açma desteklenir. Bu kayıtlar seçim öncesi karşılaştırma arşividir; seçim kullanıcı tarafından yapıldı.

- [Kurulum, lisanslar ve MacBook’a geçiş](tts/docs/INSTALLATION.md)
- [Dinleme ve ölçüm protokolü](tts/docs/PROTOCOL.md)
- [Ölçülen sonuçlar / sınırlamalar](tts/docs/QA.md)
- [Remotion bölüm sesi hazırlama](tts/docs/REMOTION.md)

MacBook Apple Silicon için `git clone https://github.com/fatihdisci/sylrnotesinde.git`, `npm ci`, `npm run tts:setup`, ardından `npm run tts:generate -- --text 'Ölçek değişir.' --output tts/outputs/manual/ornek.wav --os-offline`. Varsayılan kurulum yalnız seçili Supertonic’i indirir; karşılaştırma arşivini yeniden üretmek için açıkça `npm run tts:setup -- --all`, sonra `npm run tts:benchmark` ve `npm run tts:compare` gerekir. İlk kurulumda internet gerekir; sentez tamamen yerel. Node 22.22.3, Python 3.8+ bootstrap ve ffmpeg hazır olmalı. Ağırlıklar/venv/WAV/kişisel puanlar Git dışıdır; cihazlar arasında ortam kopyalamak yerine kurulum komutunu çalıştır. Kullanıcı puanları otomatik Git senkronu yapmaz; arayüzden JSON yedekle.

Supertonic kodu MIT, ağırlıkları **OpenRAIL-M**: ticari kullanıma genel yasak yok, kullanım kısıtları ve yapay zekâ üretimi açıklama şartı var. Diğer iki aday Apache 2.0. Tam lisans kopyaları ve kaynak revision’ları `tts/docs/licenses/` ve `tts/config/models.json` içinde.

12 profilin aynı tek cümleyi söylediği mobil MP4: [tts-12-profiles.mp4](renders/tts-12-profiles.mp4). Yaklaşık70 saniye /2,7 MB. Yeniden üretim: `npm run tts:reel`; gerçek MP4 QA: `python3 tts/qa_reel.py`. [Üretim ve inceleme kaydı](tts/docs/MOBILE_REEL.md).
