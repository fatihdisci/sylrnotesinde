# MiniMax ses testi · 2026-10-09

Kullanıcının verdiği `MiniMax_2026-10-09_23_00_01_Documentary_Narrator.mp3` yerelde içe alındı. API çağrısı/sentez yapılmadı. Orijinal dosya değiştirilmedi. Supertonic3/M1 narrator.json, seed, hız, model kayıtları ve M1 render/ses varlıkları korundu. Sağlayıcı manifestte `user:minimax`; M1 hash’leri yalnız değişmemesi gereken yerel ayarları izler, bu kaydın M1 tarafından üretildiğini belirtmez.

Kaynak47,115442 s; normalize PCM24 WAV47,115458 s. İki geçişli −20 LUFS/−2 dBTP normalizasyonu,48 kHz mono; hızlandırma, kesme ve süre doldurma yok. 87 gerçek kelime yerel/offline CTC ile yeniden hizalandı;18 öbek, aynı export’tan gömülü altyazı ve SRT. Başlangıç floor/bitiş ceil30 FPS. Görseller, efektler ve kamera eski M1 saniyeleri yerine yeni cue başlangıçlarına bağlı. Testte yıl ölçeği “bir milyar saniye” öbeğiyle, zaman şeridi “yaklaşık31,7 yıl” öbeğiyle açılır.

Çıktı `renders/episodes/seconds-film-minimax/draft.mp4`:1080×1920,30 FPS,1497 kare/49,9 s. Uzun kullanıcı kaydı doğal hızında korunabilsin diye yalnız taslak `voice-test` formatı40–60 s kabul eder; normal bölümün40–45 s ve MotionStudy’nin12–15 s sınırları değişmedi. Ses testi yayın komutlarında daima reddedilir. Son45 kare aynı kanonik outro; f1452/48,4 s’de başlar.

## Gerçek MP4 teknik sonuçları

- Başlangıç/orta/son AAC korelasyonu≥0,99966; gecikme/drift0 ms. Outro korelasyonu0,99999, gecikme0 ms.
- Ses−21,03 LUFS, true peak−8,86 dBTP; clipping yok.
- 87/87 kelime kapsamı, SRT ve gömülü altyazı eşit. Tüm öbek sınırı/orta karelerinde font, iki satır, güvenli alan ve çakışma kontrolü geçti.
- Siyah/boş içerik/boş ana geometri karesi ve büyük kare farkı adayı yok.
- ≥2 s sessizlik ve sessiz+durağan ortak aralık yok. Konuşma sürerken16,7–21,633 /35,667–38,3 /40,7–45,567 s yakın durağan tutuşlar ritim incelemesi için işaretli; otomatik hata değildir.
- 26 gerçek master kontrol karesi `controls/`; zaman sıralı `contact.jpg`; ek `mobile-preview.mp4`540×960.
- `npm run check`: typecheck/lint,12 test,17 korunan marka dosyası. `episode:test`:10 test (M1 fixture,0 skip), `alignment:test`:5, `tts:test`:7. Toplam34. M1 iki WAV `tts:qa`:0 hata. Font5/5. Beş marka referansı birebir geçti: piksel farkı0. Taslağın yayın yolunda reddedildiği ayrıca gerçek varlıklarla doğrulandı.

## İnsan incelemesi gerekenler

CTC dinleme/onay değildir. Aşağıdaki altı sözcük greedy tanı metninde farklı çıktı; bu telaffuz hatası kanıtı değildir. Özellikle “üç sıfır” ve “Her biri” modelde birleşti. Dinleyerek sözcük sınırı, son heceler ve efekt/anlatıcı dengesi kontrol edilmedi; durum `needs_review`, onay yazılmadı.

| Kelime ID | Sözcük | Otomatik ölçülen aralık |
|---|---|---|
| 10 | üç | 5.080–5.260 s |
| 11 | sıfır | 5.260–5.600 s |
| 27 | dönüşüyor. | 15.540–16.180 s |
| 34 | virgül | 19.780–20.200 s |
| 55 | Her | 32.220–32.460 s |
| 56 | biri | 32.460–32.700 s |

Master’ın açılış, takvim, blok, kamera uzaklaşması, gruplama, yıl şeridi, sonuç ve outro kareleri görsel olarak incelendi. Kontrol kareleri geçişin zaman içindeki geometrisini gösterir; gerçek zamanlı oynatımın ve öznel dinleme incelemesinin yerini tutmaz.

## Yeniden kullanım

Ayrı bir bölüm ID’sine aynı spoken/display metnini kopyala; `production.json` içinde `format: "voice-test"` ve `audioSource: {"provider":"user:minimax","voice":"Documentary_Narrator"}` tanımla. Kaydı değiştirdiğinde yeni ID kullan; mevcut WAV üzerine yazılmaz.

```sh
npm run episode:prepare -- --id <test-id> --audio /absolute/path/to/recording.mp3
npm run episode:review -- --id <test-id>
npm run episode:render -- --id <test-id> --draft
npm run episode:qa -- --id <test-id> --draft
```

Özgün sahne bileşenini registry’ye kaydet. Gerçek WAV hizalanır; dış kaynak filename/SHA256/işleme kaydı `external-audio.json` ve bağlayıcı hash’lerle korunur. Değişmeyen WAV için `--realign` kullanılabilir. `--audio` olmadan bu test M1’e sessizce dönmez. WAV/MP4 Git dışıdır; dosyalar bu Mac’te korunur.
