# Saniye koreografisi ve ortak hareket araçları

Marka 0.1-candidate. Bu çalışma yayın bölümü değil; M1 / seed42 / göreli hız1 /8 adım korunur. `production-check` ve tarihsel StyleProof kaynakları değiştirilmez.

`motion-study-15` teslim edilen15 saniyelik test (`motion-study`12 saniyelik ilk pilot), `seconds-film` tam yeniden tasarım. Saatin hızlı tam turu şematik bir dakikadır; dakika kolu bunun 1/60 hızında döner. Saat izleri 11 tam gün + %57,4074 gün dilimine açılır. Bu dilimler tek bir 1.000.000 saniye bloğuna birleşir. Kamera aynı bloğu koruyup 999 eşit bloğu daha açığa çıkarır. Son gruplama on tane 5×20=100 hücreden oluşur. Kalınlık, nesnenin perspektifi veya kamera hızı sayısal veri kodlamaz; adet kodlar. 365,25 gün/yıl varsayımıyla milyar saniye31,6881 yıldır.

- `CameraRig`: yalnız dünya geometrisini taşır; ölçeği üstel enterpolasyonla değiştirir. Okunabilir metin ve altyazı dünya dönüşümüne girmez.
- `QuantityField`: eşit hücreleri deterministik açar ve kimliklerini koruyarak gruplar. Kısmi birim kesirli genişlik alır.
- `EventSoundTrack`: gerçek sahne olay karelerine bağlı yerel sesler; kısa giriş/çıkış rampası ve anlatımın altında sabit düşük gain.
- `seconds-film/TimeRibbon.tsx`: aynı bin birimi yıllık aralıklara sahip katlanmış doğrusal şeride dizer; satır sınırında bölünen hücrenin toplam uzunluğu korunur.
- `seconds-film/model.ts`: olaylar her videonun kendi ölçülmüş caption başlangıcına bağlıdır. Saniye bazlı tahmin veya TTS hızından kelime zamanı üretimi yok.
- `scripts/generate-motion-sound.py`: tick/unfold/merge/depth/settle/reveal,48kHz mono,seed42. Özgün osilatör + filtrelenmiş gürültü; harici sample, ücretli hizmet veya üçüncü taraf ses lisansı gerekmez.

Yeni konuda bu TSX sahnelerini şablon diye kopyalamak yerine özgün bir görsel fikir yaz. Gerekli ortak geometri/kamera/ses araçlarını seç. Karmaşık 3D motor, blur veya glow varsayılanı yok.

## Üretim

```sh
npm run episode:prepare -- --id <id>
python3 scripts/generate-motion-sound.py
npm run episode:review -- --id <id>
npm run episode:render -- --id <id> --draft
npm run episode:qa -- --id <id> --draft
```

Kısa test için production.json `format: motion-study` kullanır; isteğe bağlı `minimumDurationFrames`360–450 aralığındadır: outro dahil12–15 saniye. Normal bölüm40–45 saniye olarak kalır. Gerçek konuşma süresinden sonuca geç; süre doldurmak için sessizlik ekleme. İnsan incelemesinden önce `--draft` zorunludur. `approved` değerini otomasyon yazmaz.

QA son MP4'ün her karesinde, sabit imza ve altyazının dışındaki içerik alanının piksel farkını; AAC decode'unda kare başına RMS'yi ölçer. ≥2 saniye boyunca −48dBFS altında ve ortalama normalize piksel farkı<0,0006 olan aralıklar inceleme için işaretlenir. Sessiz ve sabit aralıklar ayrıca ayrı ayrı raporlanır. Bunlar otomatik başarısızlık değildir; production.json `intentionalPauses` içindeki `{from,to,purpose}` açıklaması rapora taşınır. Eşikler hareketin anlatımsal kalitesini veya sessizliğin bilinçli olup olmadığını kanıtlamaz.

SRT ile gömülü altyazı aynı export'tan gelir. Otomatik skor, ses/kelime doğruluğu veya kullanıcı onayı değildir. Telaffuz, son hece, öznel ses dengesi ve izleme sırasında bilgiye yetişme insan incelemesinde kalır.

Bu cihazda tarihsel karşılaştırma corpus'u yeniden üretilmedi. Güncel gerçek sesleri denetlemek için `npm run tts:qa -- --episodes motion-study-15 seconds-film` kullan. Arşiv modu bayraksız komutta aynı kalır. `EPISODE_TEST_ID=motion-study-15 npm run episode:test` gerçek mevcut sesi kullanır; onay testi yalnız geçici TEST FIXTURE kopyasında çalışır.
