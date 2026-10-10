# Güneş filmi — kullanıcı MiniMax kaydı

Kaynak: kullanıcının10 Ekim2026 tarihinde sağladığı `MiniMax_2026-10-10_20_01_03_Documentary_Narrator.mp3`. MiniMax API çağrısı veya yeni TTS üretimi yapılmadı. Dosya byte eşitliğiyle `voice-sources/solar-basketball-minimax/original.mp3` içinde yerel arşivlendi. SHA256: `9cbf7448aea585b2c08728ebe2d5148cb05e87df3ceb6e12bb5aea047f4e6bba`.

Konuşma metni son kullanıcıya verilen MiniMax metnidir: “iki buçuk” → ekran “2,5”; “boyutu değil… uzaklığı” iki altyazı öbeğine ayrılır.143 sözcük,33 öbek. Ekran sayıları ve bilimsel hesaplar önceki filmle aynı. Hız/pitch/sessizlik değişikliği yok. Orijinal76,1327 saniye; çalışma kopyası48kHz mono PCM24, iki geçişli−20 LUFS normalizasyonu. Büyük WAV ve yerel arşiv Git dışıdır.

Mevcut Türkçe wav2vec2 CTC Viterbi hizalayıcı gerçek WAV üzerinde ağ yasağı altında çalıştı. Bilinen metin kullanılır; tahmini konuşma hızıyla cue üretimi yok. Yeni kelime ID'lerine göre storyboard çapaları yeniden eşlendi; sahneler ve efektler yeni sesin zamanlarını kullanır. Önceki Chatterbox/Antalia filmlerinin zaman verileri kopyalanmadı.

Aynı Three.js SolarFrame dünyası, aynı matematiksel ölçek, font/logo ve45 kare outro kullanılır. Yeni wrapper önceki Chatterbox sürümündeki Jüpiter etiket aralığı düzeltmesini korur. Altyazıların üstünde küçük açıklama katmanı yok. Ses tercihleri: anlatıcı0,40 / efekt1,00 / müzik0,17;88 BPM melodik düzenleme, temiz tonal blink/bip efektleri. Ducking bu yeni WAV’dan hesaplanır.

## Yeniden üretim

```sh
# Klonda orijinal MP3'ü tekrar sağla; mevcut varlıklar varsa yeni revision kullan.
npm run episode:import-voice -- --id solar-basketball-minimax --audio /absolute/original.mp3 --script src/episodes/solar-basketball-minimax/script.txt
npm run episode:sound:solar -- --id solar-basketball-minimax
npm run episode:review -- --id solar-basketball-minimax
npm run episode:render -- --id solar-basketball-minimax --draft --gl angle
npm run episode:qa -- --id solar-basketball-minimax --draft --gl angle
```

Yerel `--draft` master tam1080×1920 kalitededir; isim insan altyazı onayı beklediğini ifade eder. Onay kullanıcı adına yazılmaz. SRT ile gömülü altyazı aynı kareye yuvarlanmış cue verisinden türetilir. Eski film ve yerel TTS kurulumlarına dokunulmadı.
