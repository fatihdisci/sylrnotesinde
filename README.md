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

Önce AGENTS.md ve [üretim rehberini](docs/PRODUCTION_GUIDE.md) oku. `src/episodes/<id>/production.json` içinde konuşma/ekran metni, kaynaklar ve hesaplamaları tanımla; `Scenes.tsx` içinde konuya özel animasyonları yaz. `episode:prepare` gerçek sesi üretir, ölçer ve kelimeleri hizalar. İnsan incelemesinden sonra `src/episodes/registry.ts` kaydıyla genel `episode:render` / `episode:qa` komutlarını kullan. Sahneyi `EpisodeComposition` sarar; toplam süre outro dahil 1200–1350 karedir. Doğrudan Remotion CLI, yayın bütünlüğü/onay kapısının yerine geçmez.

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

## Gerçek üretim / kelime senkronu

[Güncel üretim rehberi](docs/PRODUCTION_GUIDE.md). Ayrı yerel Türkçe CTC hizalayıcı, konuşma/ekran metni eşlemesi,±1 kare düzeltme ve insan onay kapısı eklendi. Marka ve tarihsel StyleProof/Yelda korundu.

```sh
npm run alignment:setup
npm run episode:prepare -- --id production-check
npm run episode:review -- --id production-check
npm run episode:render -- --id production-check --draft
npm run episode:qa -- --id production-check --draft
npm run episode:test
npm run alignment:test
npm run alignment:offline -- --id production-check
```

Bu Mac’te ses hazırdır; yeniden hizalama için `episode:prepare -- --id production-check --realign`. Yeni metin için yeni revision ID. İnceleme: http://127.0.0.1:3033. Bayraksız render/QA insan onayı gerektirir. Eski `tts:episode` ham ses hazırlama yoludur; yayın kapısını atlamaz.

Örnek `renders/episodes/production-check/draft.mp4`; kelime JSON/SRT `public/episodes/production-check/`; QA ve kontrol kareleri `renders/episodes/production-check/`. Örnek yayın bölümü değildir; insan dinlemesi bekleniyor. [Yöntem/lisans](alignment/docs/METHOD.md), [gerçek test raporu](docs/PRODUCTION_QA.md).

## Güneş Bir Basketbol Topu Olsaydı?

[Tam MP4](deliveries/solar-basketball/gunes-basketbol.mp4) · [QA raporu](docs/episodes/solar-basketball/QA.md)

`solar-basketball`: yerel Antalia-2 Mini erkek sesiyle, tek fiziksel ölçekte özgün Three.js film. Gerçek anlatım 63,403 s; outro dahil 65,967 s. Supertonic 3/M1 ve geçmiş videolar korunur. [Üretim komutları](docs/episodes/solar-basketball/REPRODUCE.md), [storyboard/sanat yönetimi](docs/episodes/solar-basketball/ART_DIRECTION.md), [NASA hesabı ve varlık hakları](docs/episodes/solar-basketball/SOURCES_AND_LICENSES.md).

```sh
npm run tts:setup -- --model antalia-mini
# Yeni cihazda ses yokken (mevcut WAV’ı ezmez):
npm run episode:prepare -- --id solar-basketball --synthesize-model antalia-mini
npm run episode:storyboard -- --id solar-basketball
alignment/environments/ctc/bin/python production/solar_sound.py
npm run episode:render -- --id solar-basketball --draft --gl angle
npm run episode:qa -- --id solar-basketball --draft --gl angle
```

Büyük WAV/model/venv/master dosyaları yereldir. Bu bölümün normal hız seçimi bölüm dosyasında kayıtlıdır; global M1 seçimi değişmez. `draft` tam kalite inceleme masterıdır; yapılmamış insan dinlemesi/onayı başarılı sayılmaz.

Kalıcı ses tercihleri: [AUDIO_STYLE.md](docs/AUDIO_STYLE.md). Yeni bölümlerde daha sakin anlatıcı, belirgin tonal blink/bip efektleri ve hafif ritmik müzik dengesi varsayılandır.

Chatterbox Multilingual V3 için isteğe bağlı, ayrı yerel kurulum: [kurulum/çevrimdışı kullanım ve ses seçimi](tts/docs/CHATTERBOX.md). `npm run tts:chatterbox:setup` mevcut M1/Antalia ortamlarını değiştirmez. Güneş filminin Chatterbox sürümü `solar-basketball-chatterbox-tr` kimliğiyle ayrı tutulur; eski teslimler korunur.

Chatterbox Türkçe referanslı yeni film: [MP4](deliveries/solar-basketball-chatterbox-tr/gunes-basketbol-chatterbox-v3.mp4). [Gerçek QA ve dinleme bekleyen noktalar](docs/episodes/solar-basketball-chatterbox-tr/QA.md).

Kullanıcının MiniMax Documentary Narrator kaydıyla yeniden zamanlanan Güneş filmi: [MP4](deliveries/solar-basketball-minimax/gunes-basketbol-minimax.mp4), [üretim notları](docs/episodes/solar-basketball-minimax/PRODUCTION.md).
