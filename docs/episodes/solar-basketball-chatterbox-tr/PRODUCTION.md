# Güneş filmi — Chatterbox Türkçe referanslı sürüm

Aynı kullanıcı metni ve aynı özgün Three.js film. Kaynak sahneler `src/episodes/solar-basketball/` içinden tekrar kullanılır. Model, fiziksel ölçek, renk/font/logo, altyazı üstü notların kaldırılması ve kanonik 45 kare outro korunur. Kamera/sahne/efekt çapaları yeni WAV'dan çıkarılan kelime zamanlarıyla yeniden çözülür; eski sesin zamanları kopyalanmaz.

Ses: Chatterbox Multilingual V3, CPU4 thread, Türkçe. Mevcut Supertonic3/M1 TEST A sesi çalışma anı referansıdır; ses üretimini Chatterbox yapar. M1 yeniden sentezlenmez, ortam/ağırlık/ayarları değişmez. Sonradan pitch veya hız işlemi yoktur. Kısa üç adayın teknik tanısı ve kaynaklar `tts/docs/CHATTERBOX.md` içinde. Bu adayın insan dinleme onayı yoktur.

Miks: anlatıcı0,40 / efekt1,00 / müzik0,17; mevcut 88 BPM melodik düzenleme ve tonal blink/bip bankası. Efektlerin başlangıcı yeni storyboard karelerine bağlıdır. Ducking yeni gerçek WAV RMS'inden hesaplanır. Düşük miks için genel LUFS koşulu geçmezse raporda açıkça başarısız kalır; eşik değiştirilmez.

## Komutlar

```sh
npm run tts:chatterbox:setup
npm run tts:chatterbox -- --text-file src/episodes/solar-basketball-chatterbox-tr/script.txt \
  --output tts/outputs/episodes/solar-basketball-chatterbox-tr/yeni-native.wav
# Yeni ses üretiminde yeni revision id kullan; mevcut arşivi ezme.
npm run episode:import-voice -- --id <yeni-revision> --audio <native.wav> --script <kesin-script.txt>
npm run episode:sound:solar -- --id <yeni-revision>
npm run episode:render -- --id <yeni-revision> --draft --gl angle
npm run episode:qa -- --id <yeni-revision> --draft --gl angle
```

Yeni revision'a aynı solar Scenes yeniden export'u ve registry kaydı eklenir. Asıl `solar-basketball` ve perde/EQ test videosu değiştirilmedi. Native WAV, kaynak arşivi, ara stem ve model/venv Git dışı; MP4, altyazı, kurulum kilidi, referans FLAC ve teknik kayıtlar taşınabilir teslimdir.
