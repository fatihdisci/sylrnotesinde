# Hazır sesten özgün motion graphics üretimi

Kesin metin → kullanıcının dışarıda hazırladığı ses → yerel analiz/hizalama → ses çapalı storyboard → özgün TSX → efekt stem’i → gerçek MP4 ve QA. MiniMax hesabı/API kurulmaz. M1 ayarları ve eski testler korunur; `episode:prepare` artık açık bir `--audio`, `--realign` veya tarihsel `--synthesize-m1` seçimi ister. Bu görevde TTS üretilmedi.

## Bölüm hazırlığı

`src/episodes/<id>/production.json`: `format: "audio-first"`, `audioSource: {"provider":"user:minimax","voice":"Documentary_Narrator"}`, kesin `phrases` (spoken/display), kaynaklar ve hesaplanabilir iddialar. Konuşma metniyle öbekler yalnız boşluk/NFC normalizasyonu dışında birebir aynı olmalı. Sayılar spoken’da yazıyla, display’de kısa ve okunabilir biçimde olmalı. Ses yoksa içe aktarma/render adımı bekler; yedek TTS otomatik çalışmaz.

```sh
npm run episode:import-voice -- --id <id> --audio /absolute/voice.mp3 --script /absolute/script.txt
npm run episode:review -- --id <id>
npm run episode:storyboard -- --id <id>
npm run episode:sound -- --id <id>
npm run episode:render -- --id <id> --draft
npm run episode:qa -- --id <id> --draft
```

FFmpeg’in çözebildiği WAV, MP3, M4A, FLAC, OGG gibi sesler kabul edilir. Orijinal dosya `voice-sources/<id>/original.<uzantı>` altında byte eşitliğiyle arşivlenir; hash ve dosya kimliği kaydedilir. Kesin metnin kopyası `public/episodes/<id>/script.txt`. Orijinal/çalışma WAV’ı/render Git dışıdır. Çalışma sesi48 kHz mono PCM24 ve iki geçişli −20 LUFS hedefiyle normalize edilir; zaman esnetme, pitch değişikliği, son kesme veya sessizlik silme yapılmaz.

Ses/metin değişikliğinde yeni bölüm revision ID’si kullan. Orijinal, metin kopyası, çalışma WAV’ı, ayarlar ve hizalama hash’leri doğrulanır. Değişmemiş WAV’ı yeniden hizalamak için `episode:prepare -- --id <id> --realign`; bu işlem insan zaman düzeltmelerini sıfırlar. `audio-first` harici ses bağları M1’in model/ayar dosyalarına bağımlı değildir; eski varlıkların bağları aynen korunur.

Süreyi gerçek ses belirler. İçerik sonu=max(WAV sonu, son kelime + sonuç tutuşu); üzerine45 kare mevcut outro eklenir. Bu bölüm49,9 s’dir. 40 saniyeye tamamlamak için sessizlik eklenmez. Şimdiki yerel CTC motoru tek dosyada90 s’ye kadar çalışır; daha uzunu açık hata verir. Bu bir video şablonu süresi değil, mevcut hizalama motorunun işlem sınırıdır.

## Storyboard gerçek sahnenin zaman kaynağıdır

`storyboard.json` bölümün yanında saklanır. Her olayın `id`, `at`, `until`, `information`, `visual`, `camera`, `animation` ve `effects` alanı bulunur. Zaman çapası `{ "word":46, "text":"milyar" }` gibi kelime ID’si ve beklenen tam metindir. `edge:"end"` ve bilinçli `offsetFrames` da desteklenir. Sözcük değişirse yanlış olaya sessizce bağlanmak yerine hata verir. İlk olay `start`, son sınır `outro` olabilir.

Export, çapaları ölçülmüş WAV zamanından çözüp manifestte `direction.events` üretir. TSX `eventFrames()` üzerinden bu veriyi kullanır. Aynı veriden `public/episodes/<id>/storyboard.json` ve zaman kodlu `storyboard.md` çıkar. Cümle/öbek başlangıç-bitişleri ve aralarındaki duraksamalar `direction.speech.phrases` içindedir. Vurgu yorumu tasarımcıya aittir; RMS veya CTC dinlenmiş vurgu sayılmaz.

`SpatialMotion` saf kare tabanlı perspektif projeksiyonu, eş sayıda noktalı path morph, polygon/path ve maske yardımcılarını içerir. Kamera metinlere uygulanmaz. Bölüme özgü geometri/TSX serbesttir. Kalıcı sahne şablonu veya Three.js bağımlılığı yoktur. `seconds-audio-first` eşit1000 birimi yol ve bobin boyunca taşır; karşılaştırma sonunda kamera üstten bakar ve birimler aynı ölçektedir. Şematik hareket etiketi görünürdür.

## Efektler ve miks

Olaydaki efekt `{ "sound":"scale", "durationFrames":66, "gain":0.85 }` gibi tanımlanır. Başlangıcı görsel olayın karesidir; gerekirse `offsetFrames` eklenir. `production/sound.py` yerelde sabit seed ile mekanik tık/kapanış, kâğıt/katlama, whoosh, katmanlı yükselme, derin ölçek ve sonuç sesleri üretir. Harici sample/lisans bağımlılığı yoktur.

Sesler ayrı `sfx-stem.wav` içinde tutulur. Gerçek anlatımın10 ms RMS pencereleri sidechain seviyesini belirler:30 ms önden bakış ve140 ms kontrollü gain bırakma; etkin konuşmada efekt hedefi yaklaşık11 dB aşağıdadır. Kanonik EpisodeComposition’ın0,6 SFX çarpanı değiştirilmez; stem bunu hesaba katar. `sound-design.json` olay karelerini, minimum gain’i, gerçek efekt/anlatıcı oranlarını, peak’leri ve hash’leri içerir. Storyboard/hizalama değişirse eski stem kullanımı engellenir; yeniden `episode:sound` çalıştır.

## Kontrol ve insan incelemesi

`npm run check`, `episode:test`, `alignment:test`, `tts:test`, `qa:fonts`, `references:check`; bölüm için gerçek `episode:qa`. Kontrol, altyazı başlangıç/orta/bitişine ek olarak her storyboard olayının başlangıç/orta/bitişini inceler. MP4’ten kontrol PNG’leri, ses gecikmesi/drift, loudness/peak, boş kare ve sessiz+durağan aralıklar çıkar.≥2 s ortak aralık inceleme adayıdır; bilinçli duruş otomatik hata değildir.

Otomatik hizalama kelime sınırının33 ms doğruluğunu garanti etmez. Şüpheli kelimeler, telaffuz, hareket akıcılığı, efektlerin algılanması ve anlatıcı anlaşılabilirliği dinleme/izleme incelemesi ister. Bu yapılmadan `approved` yazılmaz. `--draft` kaliteli master üretir; yayın modu insan incelemesi kapısını korur. Dosya adı `draft.mp4` bu onay durumunu belirtir.
