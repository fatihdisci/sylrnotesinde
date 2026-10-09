# Gerçek bölüm üretimi

Güncel varsayılan hazır harici ses; yeni akış [Audio-first](AUDIO_FIRST.md) rehberindedir. Supertonic3/M1 yerel ayarları korunur. Marka0.1-candidate,1080×1920/30 FPS, son45 kare ortak outro. Yeni audio-first bölümlerin süresini ses belirler;1200–1350 kare sınırı tarihsel episode türüne aittir. `production-check` yalnız entegrasyon testidir; ilk yayın konusu seçilmedi.

## İlk cihaz hazırlığı

```sh
npm ci
npm run alignment:setup
npm run browser:prepare
```

Apple Silicon Mac, FFmpeg/ffprobe gerekir. TTS ve hizalama ayrı venv’lerde; sistem Python’u değişmez. İlk indirmeden sonra ses işlemleri OS ağ yasağı altında çalışır. MacBook’ta ortamları yeniden kur; MacBook kurulumu MACBOOK_MOTION_SETUP.md içinde kaydedildi. Klonda test WAV’ı yoksa `episode:prepare -- --id production-check --synthesize-m1` ile oluştur. Antalia/EMA geri kurulmaz.

## Yeni bölüm adımları

1. `src/episodes/<id>/production.json`: başlık/hook, anlamlı kısa `phrases`, kaynaklar, hesaplanabilir `claims`, varsayımlar ve ölçek. `spoken` kesin seslendirme metni; `display` en fazla iki satırlık ekran metni. Sayıları konuşma alanında yazıyla, ekranda Türkçe sayısal biçimde gir. Phrase→spoken word-ID eşlemesi `displayMap` içinde tutulur: `on bir virgül altı gün sürer.` ↔ `11,6 gün sürer.`. Otomatik okunuş tahmini yoktur.
2. `npm run episode:import-voice -- --id <id> --audio <dosya> --script <metin.txt>`: orijinal ses arşivi, iki geçişli loudnorm48 kHz PCM24 çalışma WAV’ı, gerçek sese yerel Türkçe forced alignment, kelime JSON, caption JSON, SRT, manifest. Yeni TTS üretmez. `format: audio-first`, `audioSource` ve kesin spoken/display öbekleri önceden hazırlanır.
3. `npm run episode:review -- --id <id>` → http://127.0.0.1:3033. Sesi dinle; canlı öbek altyazısı/kelime durumları görünür. Kelime başlangıç/bitişini ms veya±1 kare düzelt; inceleyen adıyla kaydet. Düzeltme geçmişi saklanır. Kaydetmek onay değildir. Sesi tamamen dinleyip zamanları kontrol ettikten sonra açık onay ver. Yapılmamış dinlemeyi onaylama.
4. Özgün `Scenes.tsx`, `EpisodeComposition` zarfını kullanır. Kamera geometriye, okunabilir etiketler ayrı ekran katmanına uygulanır. İsteğe bağlı `SceneSpace` object/comparison/journey alanı yardımcıdır; özgün animasyonu sınırlamaz. CaptionTrack’e manifest cue’ları ver. `src/episodes/registry.ts` içine bileşen/manifest kaydı ekle; Root otomatik kaydeder. Genel scriptler değişmez.
5. Taslak: `npm run episode:render -- --id <id> --draft` ve `npm run episode:qa -- --id <id> --draft`. Studio’da `Episode-<id>` görünür. Taslağın teknik geçerliliği yayın onayı değildir.
6. İnsan onayı sonrası aynı komutları `--draft` olmadan çalıştır. İkisi de bütünlüğü/onayı yeniden denetler. Render TTS çalıştırmaz. Yayınlama veya hesap oluşturma yok.

## Zaman çizelgesi ve değişiklikler

`narrationStartFrame` gerçek yerleştirme, `resultHoldFrames` minimum sonuç tutuşudur. WAV’ın başlangıç/cümle sessizlikleri tekrar eklenmez. Dosya sonu ve son kelime ayrı tutulur; kuyruk sessizliği sonuç tutuşuna sayılır. Yeni audio-first içerik sonu=max(son WAV karesi, son kelime+sonuç tutuşu); tarihsel episode türünde ayrıca40sn alt sınırı korunur; sonra45 kare outro.37,5sn+2sn+1,5sn=41sn geçerlidir. Audio-first türünde alt/üst süre zorlaması yoktur. Ses ve tüm duraksamalar korunur. Mevcut CTC tek dosya işlem sınırı90 s; daha uzun kayıt açık hata verir, kısaltılmaz veya tahmini hizalanmaz.

Kelime başlangıcı floor(ms×30/1000), bitişi ceil. Komşu cue sınırında en fazla bir karelik yuvarlama çakışması giderilir; ölçülen kelime zamanı değişmez.750ms üzeri öbek içi durakta metni anlamlı iki öbeğe ayır. Yeni aligned cue ilk karede okunur; tarihsel Yelda fade’i aynı kalır.

Production.json, konuşma metni, narrator ayarları, model revision kaydı, WAV, hizalama modeli, word-timing ve caption export hash’lerle bağlıdır. Metin/ses/ayar değişirse eski varlık geçersizdir. Yeni metinde yeni revision ID kullan; değişmeyen WAV’ı yeniden hizalamak için `episode:prepare -- --id <id> --realign`. Bu seçenek kaynak hash uyuşmazlığında durur ve insan düzeltmelerini sıfırlar; bilinçli kullan. MP4 metadata’sı manifest/sahne kaynak hash’lerini kaydeder; eski render’a yeni zamanlamanın QA’sı uygulanmaz.

Yayın kapısı boş/eksik altyazı, eksik/değişmiş ses, negatif/kesirli zaman, anlatım/cue çakışması, eksik kelime, konuşmalı açıklanamayan boşluk, outro taşması, eski hash, geçersiz süre ve onaysız incelemeyi reddeder. Yüksek CTC skoru veya JSON varlığı onay değildir.

## Genel kalite kontrolü

Final MP4 çözünürlük/FPS/kare sayısı, decode AAC başlangıç/orta/son korelasyonu/drift’i, outro sesi, peak/LUFS, siyah/boş kare ve SRT/caption kapsamı ölçülür. >1 kare ses kayması/drift başarısızdır. Her cue başlangıcı/ortası/sonu ve sahne başlangıcında Chromium font/taşma/güvenli alan/çakışma probu çalışır. En az altı gerçek MP4 inceleme PNG’si ve aynı karelerin altyazısız kontrol render’ı üretilir. Önemli metinleri `data-safe` ile etiketle; prob etiketsiz metni bilemez.

Kelime sınırının33ms doğruluğu otomatik garanti edilmez. Modelin20ms adımı çözünürlüktür. Telaffuz, son heceler, anlam/sahne uyumu, titreme ve dinlenebilirlik insan incelemesi ister. `brand:check` her render’da; `references:check` aday regresyonunda. Referans/tolerans yenilenmez.
