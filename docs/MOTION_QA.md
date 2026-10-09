# Motion üretim / senkronizasyon / görsel QA · 2026-10-09

Kod: `ea064f80b8c53414ae786b9a96f610e86d579396`. Marka0.1-candidate. İnsan dinleme/onay kaydı yok; her iki teslim `--draft`, inceleme durumu `needs_review`. Teknik geçiş yayın onayı değildir.

## Gerçek master sonuçları

| Test | Süre / kare | Kelime / öbek | AAC drift | LUFS / dBTP | Outro başlangıcı |
|---|---|---|---|---|---|
| motion-study-15 | 15.000s /450 | 29 /6 | 0.000ms | -21.44 /-5.91 | f405 (13.500s) |
| seconds-film | 40.967s /1229 | 87 /18 | 0.000ms | -21.10 /-5.90 | f1184 (39.467s) |

İki MP4 de1080×1920/30FPS, H.264/AAC. Son45 kare mevcut outro. Son MP4 decode: anlatım başı/ortası/sonu korelasyonu ve outro sesi geçti; peak<0,99, clipping/siyah/boş içerik karesi yok. Başlık ve altyazıdan bağımsız ana geometri alanında boş kare0; büyük kare değişimi adayı0. Tam kelime kapsamı ve SRT↔gömülü altyazı eşitliği doğrulandı. Metinler46px, en fazla iki satır; cue başlangıcı floor, bitişi ceil. Her cue başlangıcı/ortası/sonu ve sahne başlangıçlarında font/güvenli alan/çakışma kontrolü geçti.

## Dosyalar ve kare incelemesi

### motion-study-15

- Master: `/Users/fatih/Apps/sylrnotesinde/renders/episodes/motion-study-15/draft.mp4`
- Mobil540×960 önizleme: `/Users/fatih/Apps/sylrnotesinde/renders/episodes/motion-study-15/mobile-preview.mp4`
- Gerçek MP4 kontrol PNG’leri: `/Users/fatih/Apps/sylrnotesinde/renders/episodes/motion-study-15/controls/`
- Zaman boyunca örneklenen kare dizisi: `/Users/fatih/Apps/sylrnotesinde/renders/episodes/motion-study-15/contact.jpg`
- Teknik ölçüm: `/Users/fatih/Apps/sylrnotesinde/renders/episodes/motion-study-15/qa.json`; DOM ölçümü: `/Users/fatih/Apps/sylrnotesinde/renders/episodes/motion-study-15/layout-qa.json`
- Kontrol kareleri: `/Users/fatih/Apps/sylrnotesinde/renders/episodes/motion-study-15/control-frames.json`; altyazısız eş kareler: `/Users/fatih/Apps/sylrnotesinde/renders/episodes/motion-study-15/review/`

Masterdan çıkarılan kontrol kareleri: hook=f0, clock=f117, days=f181, single-unit=f208, zoom=f243, years=f282, thousand=f353, result=f393, outro=f427.

MP4 SHA256: `2e60f44288c006cce4d545c4119771fc40f7d99de4a1548d1f6145ef04b16e05`; kaynak+yerel efekt SHA256: `c5bc018b01d4bdd86f6cac4ea4beb1aacb5e686d9b7f3475c91d6a7ee5052e93`.

### seconds-film

- Master: `/Users/fatih/Apps/sylrnotesinde/renders/episodes/seconds-film/draft.mp4`
- Mobil540×960 önizleme: `/Users/fatih/Apps/sylrnotesinde/renders/episodes/seconds-film/mobile-preview.mp4`
- Gerçek MP4 kontrol PNG’leri: `/Users/fatih/Apps/sylrnotesinde/renders/episodes/seconds-film/controls/`
- Zaman boyunca örneklenen kare dizisi: `/Users/fatih/Apps/sylrnotesinde/renders/episodes/seconds-film/contact.jpg`
- Teknik ölçüm: `/Users/fatih/Apps/sylrnotesinde/renders/episodes/seconds-film/qa.json`; DOM ölçümü: `/Users/fatih/Apps/sylrnotesinde/renders/episodes/seconds-film/layout-qa.json`
- Kontrol kareleri: `/Users/fatih/Apps/sylrnotesinde/renders/episodes/seconds-film/control-frames.json`; altyazısız eş kareler: `/Users/fatih/Apps/sylrnotesinde/renders/episodes/seconds-film/review/`

Masterdan çıkarılan kontrol kareleri: hook=f0, clock=f222, days=f418, single-unit=f541, zoom=f638, thousand=f868, years=f953, ribbon=f1065, result=f1138, outro=f1206.

MP4 SHA256: `a739d55b734724ff2a9032f45fa4922b918f667f2c4f2e343cf407156d165296`; kaynak+yerel efekt SHA256: `c5bc018b01d4bdd86f6cac4ea4beb1aacb5e686d9b7f3475c91d6a7ee5052e93`.

Başlangıç, saat→gün, tek blok→kamera uzaklaşması, bin blok gruplama, yıllık şerit, sonuç ve outro kareleri incelendi. 15s çalışmada0,5s; tam videoda2s aralıklı gerçek MP4 kare dizileri görsel olarak değerlendirildi. Bu inceleme kesintisiz insan izleme/dinleme testi yerine geçmez. İlk 12s pilotun kaynakları ve render’ı da korundu. Tarihsel40s production-check MP4 ve kaynakları korunur.

## Ritim ölçümü

Kare bazında içerik alanı piksel farkı ve AAC RMS ölçüldü. Eşikler:−48dBFS, normalize ortalama piksel farkı0,0006, minimum2s. Otomatik hata üretmez.

**motion-study-15:** ≥2s sessiz aralık0, sessiz+neredeyse sabit aralık0.
Sese bakılmadan bulunan sabit aralıklar: 11.467–13.500s.
**seconds-film:** ≥2s sessiz aralık0, sessiz+neredeyse sabit aralık0.
Sese bakılmadan bulunan sabit aralıklar: 13.033–16.033s; 17.333–19.767s; 28.633–32.700s; 34.900–37.233s; 37.267–39.467s.

Tam videodaki duruşların amacı:11,6 günün okunması; tek bloğun kavranması; kamera sonrası eşit hücrelerin görülmesi; binlik grupların ve yıl değerinin okunması; katlanmış eksen ve sonucun okunması. 28,6–32,7s civarındaki yaklaşık4s duruş, sesli açıklama sırasında en uzun görsel duruştur; izleyici ritmi incelemesinde özellikle değerlendirilmeli. Süre dolduran ek sessizlik eklenmedi.

## Şüpheli kelimeler — insan dinlemesi gerekiyor

Bunlar greedy CTC tanı metni uyuşmazlıklarıdır; otomatik telaffuz hatası veya zaman düzeltme kararı değildir. Yüksek confidence, kare hassasiyetinde insan doğrulaması sayılmaz.

| Video | Kelime ID | Sözcük | WAV başlangıç–bitiş | İnceleme nedeni |
|---|---|---|---|---|
| motion-study-15 | 0 | Üç | 0.540–0.660s | diagnostic_text_mismatch |
| motion-study-15 | 1 | sıfır, | 0.670–1.240s | diagnostic_text_mismatch |
| seconds-film | 10 | üç | 4.100–4.240s | diagnostic_text_mismatch |
| seconds-film | 11 | sıfır | 4.240–4.580s | diagnostic_text_mismatch |
| seconds-film | 17 | Saatin | 7.030–7.540s | diagnostic_text_mismatch |
| seconds-film | 20 | turu | 8.060–8.300s | diagnostic_text_mismatch |
| seconds-film | 21 | bir | 8.300–8.400s | diagnostic_text_mismatch |
| seconds-film | 47 | saniyeye | 20.540–21.040s | diagnostic_text_mismatch |
| seconds-film | 56 | biri | 25.960–26.140s | diagnostic_text_mismatch |
| seconds-film | 83 | Fark | 37.100–37.330s | diagnostic_text_mismatch |
| seconds-film | 84 | tam | 37.380–37.540s | diagnostic_text_mismatch |

15s testin ilk “üç sıfır” öbeği ve tam videoda “üç sıfır”, “saatin”, “turu bir”, “saniyeye”, “biri”, “fark tam” özellikle dinlenmeli. Tüm son heceler, altyazının okunma hızı ve ana görsele yetişme de insan incelemesinde. `npm run episode:review -- --id motion-study-15` veya `--id seconds-film` ile yerel editörü aç. Her iki gerçek yayın komutunun onaysız incelemeyi reddettiği ayrıca doğrulandı. Hiçbir gerçek kayıt kullanıcı adına onaylanmadı.

## Gerçek çalıştırılan kontroller

- `npm run check`: typecheck/lint +11 Node testi geçti;17 korunan marka dosyası değişmedi.
- `npm run tts:test`:7 test geçti; HTTP testi geçici TEST FIXTURE WAV kullanır, eski corpus üretimi gerekmez.
- `npm run tts:qa -- --episodes motion-study-15 seconds-film`:2 gerçek native/listening WAV,0 hata; normalizasyon hedefleri kontrol edildi.
- `npm run tts:offline`: OS ağ yasağı + bağımsız decoded PCM tekrarı birebir eşit.
- `npm run alignment:test`:5 test geçti (CTC, gerçek kayma yakalama, ritim).
- `EPISODE_TEST_ID=motion-study-15 npm run episode:test`:9 test geçti,0 atlama; onay mutasyonu yalnız geçici TEST FIXTURE kopyasında.
- `npm run alignment:offline -- --id motion-study-15` ve `--id seconds-film`:29/87 kelime zamanları birebir aynı; ağ girişimi yok.
- `npm run qa:fonts`:5 dosyada Türkçe ve ölçü glyph kapsamı geçti.
- `npm run references:check`:5 marka PNG’sinde ortalama piksel farkı0; referans/eşik yenilenmedi.
- İki teslim için `episode:render/qa --draft`:gerçek1080×1920 MP4 üzerinde geçti.
- Altı prosedürel efekt WAV’ı tekrar üretimde byte düzeyinde aynı SHA256 verdi.

## Görsel doğruluk ve yeniden kullanım

1 milyon saniye=11,574074… gün;1 milyar saniye=31,688087… yıl (365,25 gün/yıl açık varsayımı); oran tam1.000. Gün birimi için [BIPM SI Brochure, tablo8](https://www.bipm.org/en/publications/si-brochure) kontrol edildi. İlk alanda adet, son katlanmış şeritte doğrusal süre kodlanır. Şerit satır sınırında bölünen hücre uzunlukları korunur; matematik ve kamera uçları test edildi. Kilometre örneği yeni filmde yok.

Kamera/QuantityField/EventSoundTrack ortak araçları ve özgün saat→gün→bin blok→yıl şeridi koreografisi: [MOTION_PRODUCTION.md](MOTION_PRODUCTION.md). Optik efektlerin kontrollü istisnaları ANIMATION_RULES.md içinde; Three.js veya dekoratif glow eklenmedi. Sesler kodla üretilmiş özgün osilatör/gürültü; ticari harici sample yok. Efekt kareleri görsel olaylarla aynı veri kaynağından; düşük gain ve kısa volume rampaları var. Öznel ses dengesi kulakla onaylanmış değildir.

Marka paleti/fontları/logo/outro/kapanış WAV’ı, tarihsel StyleProof/altyazı fade’i ve M1 config/model/kilit/seed/hız değişmedi. İlk aday marka onayı hâlâ kullanıcıya ait. Büyük WAV/MP4/model/venv Git dışında; kısa özgün efekt WAV’ları kodla birlikte izlenir.
