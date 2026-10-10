# Mac mini / MacBook üretimi

Bu bölümün model/venv/WAV/master dosyaları Git dışıdır. Kod, küçük dokular, senaryo, storyboard, kilitler ve zamanlama kayıtları Git ile taşınır. Venv cihazlar arasında kopyalanmaz. Mevcut ses dosyalarını koru; yoksa aynı ID için yeniden üretim adımını uygula. Süreyi kısaltmak için sesi hızlandırma.

```sh
git pull --ff-only origin main
npm ci
npm run browser:prepare
npm run tts:setup -- --model antalia-mini
npm run alignment:setup
# narration.wav yokken: açık, yalnız bölüm kapsamlı Antalia üretimi
npm run episode:prepare -- --id solar-basketball --synthesize-model antalia-mini
# Mevcut WAV + aynı script ile yalnız hizalamayı yenilemek gerekirse:
# npm run episode:prepare -- --id solar-basketball --realign
npm run episode:storyboard -- --id solar-basketball
alignment/environments/ctc/bin/python production/solar_sound.py
npm run check
npm run episode:render -- --id solar-basketball --draft --gl angle
npm run episode:qa -- --id solar-basketball --draft --gl angle
npm run episode:review -- --id solar-basketball --port 3035
npm run preview
```

Dokular repoda yereldir; yeniden hazırlama gerekirse `.venv/bin/python scripts/prepare-solar-assets.py` (Pillow). İlk indirme dışındaki sentez/hizalama/miks/render ağ gerektirmez. Browser kurulumunu da çevrimdışı renderdan önce tamamla. `--gl angle` Mac üzerinde bu Three.js bölümü için kullanılır.

- Studio: `http://localhost:3020/Episode-solar-basketball`.
- Sözcük düzeltme: `http://127.0.0.1:3035`. Mevcut inceleme aracı WAV’ı dinletir, aynı zamanlamayla altyazı öbeklerini gösterir; ±1 kare düzenleme ve JSON kaydı vardır. Onay düğmesine yalnız gerçek dinleme sonrası basılır.
- Tam kalite MP4: `renders/episodes/solar-basketball/draft.mp4`. `draft` yalnız yayın onayı durumunu belirtir; çözünürlük veya render kalitesi düşürülmez.
- Ham 48 kHz Antalia: `tts/outputs/episodes/solar-basketball/narration.wav`.
- Normalize anlatıcı: `public/episodes/solar-basketball/narration.wav`.
- Ayrı stereo katmanlar: aynı klasörde `sfx-stem.wav`, `ambient-stem.wav`; tam miks `mix.wav`.
- Aynı kelimelerden SRT/JSON: `captions.srt`, `captions.json`, `word-timings.json`.
- Orijinal ve okunacak metin: `original-script.txt`, `script.txt`; gerçek normalizer çıktısı `tts-generation.json` içinde.
- Gerçek MP4 kontrol kareleri ve altyazısız kontroller: `renders/episodes/solar-basketball/review/`.

İnsan incelemesi henüz onaylanmadığı için bayraksız yayın renderı bilinçli olarak engellenir. İncelemeden sonra kelime kaydı değişirse storyboard ve skor yeniden üretilir, MP4 yeniden render/QA yapılır. `approved` durumunu agent kullanıcı adına yazmaz. Otomatik CTC confidence her sözcükte bir kare doğruluk garantisi değildir.

Supertonic 3/M1 merkezî seçim ve kurulu yedek olarak korunur; bu komutlar onu yeniden kurmaz. `tts:setup --all` kullanma; EMA bu görevde kurulmadı.
