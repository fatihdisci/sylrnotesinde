# Adayı yeniden üretme

Proje Node22.22.3 / npm10.9.8, FFmpeg/ffprobe, yerel hizalama ortamı ve Chrome Headless Shell gerekir. MacBook'ta WebGL ANGLE kullanılır. M1 kurulumu/TTS üretimi gerekmez.

```sh
npm ci
npm run alignment:setup
npm run browser:prepare
npm run episode:import-voice -- --id seconds-sculpture --audio /tam/yol/kayit.mp3 --script src/episodes/seconds-sculpture/script.txt
alignment/environments/ctc/bin/python production/sculpture_sound.py
npx remotion render src/index.ts SculpturePrototype renders/episodes/seconds-sculpture/prototype.mp4 --gl=angle --crf=18
npm run episode:render -- --id seconds-sculpture --draft --gl angle
npm run episode:qa -- --id seconds-sculpture --draft --gl angle
npm run check
npm run episode:test
npm run alignment:test
npm run tts:test
npm run tts:qa
npm run references:check
```

`--draft` teknik/yüksek çözünürlüklü yaratıcı aday anlamındadır; düşük kalite anlamına gelmez. Otomatik hizalamayı insan onayı yapmaz. İnsan incelemesi `episode:review` ile yapılır. Kesin metin, orijinal arşiv, normalize WAV, hizalama, storyboard ve stem hash'leri eski varlık kullanımını engeller. İşlenmiş sesin loudness normalizasyonu önceki audio-first akışıyla aynıdır; tempo/perde/deklaratif duraklar değişmez.

Yeni bölüm için mevcut audio-first rehberini izleyin. Bu adayın `Sculpture.tsx` ve `choreography.ts` dosyaları özgün sanat yönetimidir; her bölümün zorunlu şablonu değildir. Kameralar, gerçek ses kelimelerine bağlı storyboard olaylarından zaman alır. Geometri yalnız bu bölümün sayısal ilişkisine aittir. Protected marka dosyalarına aday tasarım kopyalanmaz.

Büyük masterlar, kaynak ses, WAV ve kontrol kareleri Git dışıdır. Zamanlama/SRT/storyboard/raporlar ve kod Git'tedir. Prototip gerçek MP4'ü ile tam filmin MP4'ü ayrı tutulur.
