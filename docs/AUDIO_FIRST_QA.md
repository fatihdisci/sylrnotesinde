# Zaman şeridi · MiniMax audio-first QA

Kullanıcı kararı: süre her zaman hazır sese göre belirlenir. Bu bölümde47,115 s orijinal MiniMax kaydı değişmeden kullanıldı; son kelime46,870 s, sonuç tutuşu45 kare, outro48,4–49,9 s. Çıkış1497 kare,1080×1920,30 FPS. `draft.mp4` adı insan onayının henüz kaydedilmediğini belirtir; düşük çözünürlüklü taslak değildir.

## Görsel sonuç ve düzeltmeler

Önceki video ağırlıklı olarak sabit üst başlık, küçülen ızgara ve uzun grafik tutuşları kullanıyordu. Yeni ana nesne zaman kapsülüdür: büyük kadran →12 saat işaretinden takvim yaprakları →11 tam gün +12.günün%57,4’ü → kapanan tek zaman bloğu →1000 birimlik kıvrımlı yol → yılları gösteren bobin. Kamera geniş plan, yol takibi ve tek birime yakınlaşma arasında anlatıma göre geçer. Finalde perspektif sıfırdır; ilk mercan birim büyütülmez. Takvimde büyütülen12.gün açıkça yakın plan olarak etiketlidir. Yolun hareketi şematiktir; disk alanının1000 kat olduğu iddia edilmez.

Gerçek render incelemelerinde erken tamamlanan uzaklaşma, üst üste gelen takvim yaprakları, kameranın29,8 s civarında ana yoldan ayrılması ve43,3 s’deki ani toplu kararma tespit edilip düzeltildi. Hareketli dünya başlık/ölçüm/altyazıdan maskeyle ayrıldı. Son master üzerinden43 kontrol karesi ve zaman sıralı contact sheet çıkarıldı. Tarayıcıda gerçek MP4 sessiz oynatımı açıldı; açılış, ölçek ve bobin/sonuç anlarından örnekler gözlendi. Bu örnekleme, bütün videonun insan tarafından kesintisiz izlenip dinlendiği anlamına gelmez.

## Teknik doğrulama

- `npm run check`: typecheck/lint +15 Node testi;17 korunan marka dosyası değişmedi.
- `episode:test`:14 test,0 skip; gerçek M1 ve ithal ses varlıklarının geçici TEST FIXTURE kopyalarıyla onay/hash kapıları dahil.
- `alignment:test`:5; `tts:test`:7. Toplam41 test geçti.
- Font QA5/5; beş StyleProof/marka referansı birebir aynı, piksel farkı0. Referans ve eşikler değiştirilmedi.
- M1’in mevcut iki WAV’ı `tts:qa` ile yeniden kontrol edildi:0 hata. Yeni TTS üretilmedi.
- Gerçek MiniMax WAV’ının87 kelimesi OS ağ yasağı altında tekrar hizalandı:87/87 aynı zaman,0 ağ girişimi.
- Ayrı efekt stem’i, miks kaydı ve manifest tekrar üretimde byte eşitliği verdi.
- Orijinal MP3 ve proje içi arşivi SHA256 olarak aynı. Konuşma metni, M1 narrator ayarları/model kayıtları ve tarihsel renderlar değiştirilmedi.
-103 yerleşim kontrolü: altyazı ve olay başlangıç/orta/bitişleri; taşma, çakışma, font yükleme veya iki satır sınırı hatası yok.
- Ses gecikmesi/drift0 ms.21 storyboard olayının gerçek MP4 miks korelasyonu en az0,99946; olay başlangıçlarında0 ms kayma. Outro da kendi sınırında doğrulandı.
- Gerçek MP4−20,97 LUFS, true peak−8,98 dBTP; clipping/ani ses kesilmesi saptanmadı.
- Siyah/boş içerik/boş ana geometri karesi ve büyük kare farkı adayı yok.
-≥2 s sessizlik ve sessiz+durağan ortak aralık yok. Yakın durağan aralıklar23,533–25,600 s (tek bloğun okunması) ve46,267–48,400 s (sonuç). İkisinde de konuşma bulunur; sonuçtan sonraki sessiz tutuş1,5 s’dir.

27 efekt olayı21 görsel olaya bağlı. Kaynaklar yerel, özgün ve seed42 ile deterministik; harici ses örneği kullanılmadı. Saat tıkları, kâğıt, kapanış, whoosh, ölçek/riser ve sonuç sesleri ayrı `sfx-stem.wav` katmanında. Gerçek ses RMS’iyle ducking: konuşmayla çakışan etkin pencerelerde medyan efekt/anlatıcı oranı−16,41 dB;95.persentil−11,37 dB. Bu ölçümler duyulabilirlik/beğeni onayı değildir; miks kulakla ayrıca değerlendirilmelidir.

## İnsan incelemesi

Otomatik zamanlama insan onayı sayılmadı; `needs_review` ve `listened:false` korundu. Aşağıdaki6 sözcük aynı CTC modelinin greedy tanı metniyle farklı çıktı. “Üç sıfır” ve “Her biri” birleşik algılandı; bu kesin telaffuz hatası değildir. Kanıt olmadan kelime zamanları elle kaydırılmadı.

| Sözcük | Ölçülen aralık | İnceleme nedeni |
|---|---|---|
| üç | 5.080–5.260 s | diagnostic_text_mismatch |
| sıfır | 5.260–5.600 s | diagnostic_text_mismatch |
| dönüşüyor. | 15.540–16.180 s | diagnostic_text_mismatch |
| virgül | 19.780–20.200 s | diagnostic_text_mismatch |
| Her | 32.220–32.460 s | diagnostic_text_mismatch |
| biri | 32.460–32.700 s | diagnostic_text_mismatch |

İncelemede özellikle bu kelimelerin başlangıç/son hecelerini,25,6–38,98 s kamera akışını, efekt/anlatıcı dengesini ve finaldeki1:1000 ilişkisinin anlaşılmasını kontrol et. Instagram referansının dosyası/bağlantısı bu çalışma bağlamında yoktu; referansla birebir eşleşme iddia edilmez.

## Dosyalar

- Master: `renders/episodes/seconds-audio-first/draft.mp4`
- Mobil kopya: `renders/episodes/seconds-audio-first/mobile-preview.mp4`
- Kontrol kareleri: `renders/episodes/seconds-audio-first/controls/`; `contact.jpg`, `control-frames.json`
- Gerçek MP4 ölçümleri: `renders/episodes/seconds-audio-first/qa.json`, `layout-qa.json`
- Altyazı: `public/episodes/seconds-audio-first/captions.srt` / `captions.json`
- Kelimeler: `public/episodes/seconds-audio-first/word-timings.json`
- Çözümlenmiş storyboard: `public/episodes/seconds-audio-first/storyboard.md` / `storyboard.json`
- Kaynak storyboard/özgün sahneler: `src/episodes/seconds-audio-first/`
- Orijinal: `voice-sources/seconds-audio-first/original.mp3`
- Efekt/miks: `public/episodes/seconds-audio-first/sfx-stem.wav` / `sound-design.json`
- Yeni üretim komutları ve yöntem: [AUDIO_FIRST.md](AUDIO_FIRST.md)

Büyük ses/render dosyaları Git dışıdır ve bu Mac’te saklanır. Kod, kesin metin, storyboard, küçük zamanlama ve ölçüm kayıtları repodadır. Sosyal platformlarda paylaşım yapılmadı.
