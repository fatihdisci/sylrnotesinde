# Yarım ses pes + hafif EQ dinleme testi

Kullanıcı açıkça önceki perde/EQ önerisinin ayrı bir test videosunu istedi.

- Asıl video: `deliveries/solar-basketball/gunes-basketbol.mp4`; değiştirilmedi.
- Test: `deliveries/solar-basketball/gunes-basketbol-voice-minus-half-eq.mp4`.
- Ayarlar ve hash'ler: aynı isimli `.json`; gerçek MP4 ölçümleri `.qa.json`.
- Konuşma: −0,5 yarım ses (48 kHz'de yuvarlanan oranla −0,49983), 2.800 Hz'de −1,5 dB/Q=1 EQ, 65 Hz high-pass.
- Yöntem: yerel FFmpeg yeniden örnekleme + WSOLA tempo telafisi. Formant koruması yok; formantlar da çok hafif aşağı kayar. Yeni TTS sentezi veya model ayarı değişikliği yapılmadı.
- Kaynak ve işlenmiş konuşma aynı örnek sayısında; konuşma hızı veya bölüm süresi kasten değiştirilmedi. WSOLA yerel küçük zaman farkları üretebilir; dosya süresinin eşit olması tek başına kelime senkronunu kanıtlamaz.
- Anlatıcı gain 0,40, efekt 1,00, müzik 0,17. Remotion'un mono→stereo eşit güçlü dönüşümü korunur (kanal başına anlatıcı 0,40/√2). Sonradan genel normalizasyon yapılmadı.
- Müzik v5 ve efekt stem'leri aynı. Video akışı yeniden kodlanmadan kopyalandı. 45 karelik outro ve kapanış WAV'ı aynı.
- Ara WAV'lar `renders/experiments/solar-basketball-voice-minus-half/` içinde, Git dışında.
- Merkezi anlatıcı seçimi, TTS ayarları, kaynak WAV, asıl MP4, altyazı kaynakları ve marka dosyaları değiştirilmedi. Bu aday varsayılan değildir.

## Yeniden üretme

Önce kaynak bölümün yerel anlatıcı/stem WAV'ları mevcut olmalı. Çıkış adı yeni olmalı; script var olan videonun üzerine yazmaz.

```sh
alignment/environments/ctc/bin/python production/voice_variant.py \
  --source-video deliveries/solar-basketball/gunes-basketbol.mp4 \
  --output deliveries/solar-basketball/yeni-test-adi.mp4
alignment/environments/ctc/bin/python production/qa_voice_variant.py \
  --video deliveries/solar-basketball/yeni-test-adi.mp4
```

## Kontroller ve sınırlar

Gerçek MP4 decode edilerek işlenmiş konuşmayla başlangıç/orta/son korelasyonu, tam miks olay örnekleri, outro, clipping, LUFS, çözünürlük/FPS/kare sayısı ve görüntü akışının birebir aynı kalması kontrol edilir. Kaynak ve yeni MP4'te mono decode üzerinden ölçülen anlatıcı gain'i de karşılaştırılır.

Orijinal ve işlenmiş konuşmanın enerji zarfları 5 ms adımlarla, perde değişiminin periyot etkisini ayırmak için 40 ms yumuşatılarak karşılaştırılır. Bu bir cümle düzeyi gecikme tanısıdır; her kelimede bir kare hassasiyeti veya insan onayı iddiası değildir. İlk yumuşatılmamış 5 ms RMS denemesinde orta bölüm korelasyonu 0,883 çıktı (gecikme 5 ms); bu nedenle enerji zarfı tanısı açıkça 40 ms yumuşatmaya geçirildi, 0,90 korelasyon ve 33,3 ms gecikme sınırları değiştirilmedi.

TypeScript/lint, 21 temel test, 17 marka dosyası kontrolü, 7 TTS testi ve kaynak ses QA çalıştırıldı. Yeni test için gerçek sonuçlar `.qa.json` içindedir. Genel −25…−17 LUFS hedefi ölçülür; sağlanmıyorsa başarılı sayılmaz ve eşik değiştirilmez.

İnsan dinlemesi yapılmadı. Perde işleminin doğallığı, metalik izler, Türkçe ünsüzlerin açıklığı ve mevcut altyazıların sözcük hassasiyeti dinleyici incelemesi bekliyor. Önceki altyazı onay durumu `needs_review` olarak kalır. Bu bir dinleme testi; yayın onayı değildir.

## Bu çıktının ölçümleri

1080×1920, 30 FPS, 1979 kare (65,967 s). İşlenmiş konuşma/MP4 başlangıç, orta, son gecikmeleri [0.0, 0.0, 0.0] ms. Enerji zarfı gecikmeleri [0, 0, 0] ms. 22 tam miks olay örneği geçti; outro gecikmesi 0.0 ms. -27.59 LUFS, -11.47 dBTP; clipping yok. Genel LUFS hedefi geçmedi, bu durum raporda false. Orijinal mono-decode anlatıcı gain'i 0.39934, testinki 0.39915; hedef 0,40. Görüntü bit akışı aynı.
