# Üretim altyapısı · gerçek test kaydı

2026-10-09, Apple Silicon Mac mini (M4), CPU. Marka `0.1-candidate`. İlk yayın konusu seçilmedi; `production-check` yayımlanmayacak entegrasyon testidir.

**Teknik kontroller geçti. İnsan dinleme/kelime incelemesi tamamlanmadı; yayın onayı verilmedi.** `review.status=needs_review`, `publicationReady=false`. Bayraksız gerçek render komutu, “PUBLICATION BLOCKED: human audio/timing review is not approved” hatasıyla render başlamadan durdu. Testlerdeki onaylı kayıtlar yalnız geçici **TEST FIXTURE** kopyalarıdır; teslim verisine insan onayı yazılmadı.

## Teslim varlıkları

- [Gerçek 40 saniyelik MP4](../renders/episodes/production-check/draft.mp4), H.264/AAC, 1080×1920, 30 FPS, tam 1.200 kare.
- [Sekiz gerçek MP4 karesi](../renders/episodes/production-check/verified-contact-sheet.png): kare 40/260/410/500/640/800/965/1180. Her PNG final MP4'ten ayrı ayrı decode edildi; görsel olarak incelendi.
- [Altyazılı / altyazısız kontrol panosu](../renders/episodes/production-check/caption-control-sheet.png). Üst sıra gerçek MP4, alt sıra aynı sahne/kare için altyazısız Remotion kontrol render'ı. Tam boy kareler yerelde `renders/episodes/production-check/review/` altında; genel QA yeniden üretir.
- [Kelime zamanları](../public/episodes/production-check/word-timings.json), [SRT](../public/episodes/production-check/captions.srt), [caption JSON](../public/episodes/production-check/captions.json). Üçü aynı **taslak** kelime verisinden gelir. İnsan onayı sonrası aynı export yolu kullanılır; bağımsız bir SRT zaman kaynağı yoktur.
- [Nihai medya ölçümleri](../renders/episodes/production-check/qa.json), [44 karelik Chromium yerleşim/font ölçümleri](../renders/episodes/production-check/layout-qa.json).

WAV ve native master yereldir, Git dışıdır: `public/episodes/production-check/narration.wav`, `tts/outputs/episodes/production-check/narration.wav`. Klonda `episode:prepare` ile yeniden üret.

## Çalıştırılan kontroller

| Komut / kontrol | Gerçek sonuç |
| --- | --- |
| `npm run check` | TypeScript, ESLint, 7 TS testi ve 17 korunan dosya hash'i geçti |
| `npm run episode:test` | 8 Python testi geçti; gerçek HTTP audio-range, onaysız kaydetme reddi, eski hash, eksik WAV/kelime, geçersiz/çakışan zaman, konuşmalı boşluk ve geçici yayın kapısı testi |
| `npm run alignment:test` | 3 test geçti; tekrar eden CTC harfi/blank, imkânsız eşleme reddi, gerçek sinyalde >1 kare kayma tespiti |
| `npm run tts:test` | Mevcut 7 TTS/karşılaştırma/seçim testi geçti |
| `npm run tts:qa` | Tarihsel 72 dinleme WAV'ı: 0 hata; −20,32..−19,92 LUFS; en yüksek true peak −1,90 dBTP |
| `npm run qa:fonts` | Beş IBM Plex dosyası, Türkçe karakter eksiği yok |
| `npm run references:check` | Beş mevcut referansta piksel farkı 0; tolerans/referans/hash manifesti yenilenmedi |
| `npm run episode:render -- --id production-check --draft` | Gerçek M1 sesli 1.200 kare MP4 render edildi |
| `npm run episode:qa -- --id production-check --draft` | MP4 decode, ses korelasyonu, süre/outro/SRT, bütün içerik karelerinde boş/siyah kontrolü, 44 yerleşim probu geçti |
| Bayraksız `episode:render` | Beklenen onay hatasıyla reddedildi; kullanıcı adına onay üretilmedi |
| `npm run tts:offline` | M1 gerçek sentezi OS `deny network*` altında; ağ probe'u reddedildi, ağ isteği yok; decode PCM birebir aynı |
| `npm run alignment:offline -- --id production-check` | Gerçek WAV yeniden hizalandı; 67 kelimenin zamanları birebir aynı, ağ isteği yok |

Toplam 25 otomatik test geçti. HTTP/UI testlerinde teslim kelime dosyası değişmeden kaldı. Yerel dinleme ekranı tarayıcıda açıldı; gerçek WAV yükleme/seek/oynatma, canlı öbek ilerlemesi ve ±1 kare kontrolü çalıştı. Bu, insanın Türkçe sesi dinleyerek doğrulaması olarak raporlanmaz.

## Gerçek ses / zaman çizelgesi

Supertonic 3 / M1, mevcut doğal hız `speed=1` (adaptörün seçili native 1,05 ayarı), seed42, CPU/2 thread korunur. Native 44.100 Hz master: **33,126349 saniye**. Sentez **5,661 saniye**, CPU zamanı **11,313 saniye**, ortalama CPU **%199,84**, tepe RSS **620,5 MiB**. Konuşma hızlandırılmadı. Render kopyası 48.000 Hz PCM24'tür.

Bilinen 67 kelime aynı Türkçe wav2vec2 modeliyle CTC forced alignment kullanılarak gerçek WAV'a bağlandı; WhisperX paketi kurulmadı. [Yöntem, kilit ve lisans kaydı](../alignment/docs/METHOD.md). İlk son-hâl hizalama **2,775 saniye / 2.107,8 MiB RSS**; bağımsız çevrimdışı tekrar **2,975 saniye / 2.855,8 MiB RSS**. İşlem RSS'i cache/çalışma koşullarına göre değişir. [Çevrimdışı kayıt](../alignment/docs/production-check-offline-qa.json).

Son ölçülen kelime bitişi **32.460 ms**. Sonuç başlangıcı kare974, içerik sonu1155, outro45 kare, toplam1200. Son kelimeden sonra sonuç **181 kare / 6,033 saniye** tutulur; WAV kuyruk sessizliği bunun içindedir. 40 saniye alt sınırı bu testte uzun bir sonuç tutuşu oluşturur. 37,5 saniye anlatım +2 saniye tutuş +1,5 saniye outro =41 saniye örneği ayrıca test edildi. Konuşma için eski 38,5 saniyelik alt sınır kaldırıldı.

Final MP4'ün AAC sesi decode edilerek kaynak WAV ile karşılaştırıldı:

| Konum | Kaynak örnek başlangıcı | Kayma | Korelasyon |
| --- | --- | --- | --- |
| Başlangıç | 510 ms | 0 ms | 0,999962 |
| Orta | 13.820 ms | 0 ms | 0,999919 |
| Son | 30.810 ms | 0 ms | 0,999877 |

Ölçülen drift **0 ms**. Outro sesi korelasyonu **0,999993**, kayma0 ms. Final −21,17 LUFS, −5,91 dBTP; mono decode tepe0,71564, clipping yok. Anlatım outrodan önce biter. SRT ile gömülü cue'lar aynı kare sınırlarını kullanır; 67/67 kelime kapsanır. Bu test kodlama/timeline kaymasını ölçer; bir CTC kelime sınırının doğru heceye geldiğini tek başına kanıtlamaz.

## Yapılan görsel inceleme ve düzeltmeler

Gerçek MP4 karelerinde iki satır sınırı, Türkçe karakterler, güvenli alan, sayı/başlık/altyazı ayrımı, ölçüm çizgileri ve kanonik outro incelendi. Kamera geometriyi küçültürken etiketler sabit kaldı. 1:1.000 uzunluk ilişkisi TSX'te gerçek doğrusal geometriyle kuruldu; uzun çizginin başlangıçta kadraj dışına uzandığı açıkça etiketlendi. Alan/hacim karşılaştırması yapılmadı. 11,6 gün /31,7 yıl ve kilometre/metre hesabı, kaynak/varsayım kaydıyla doğrulandı.

CTC spike'ları gerçek RMS kenarlarıyla sınırlandırılarak üç açıklanamayan boşluk giderildi; bu otomatik akustik düzeltmeler JSON'da ayrı kayıtlıdır. Taslak metindeki “bin kez” diagnostic uyuşmazlığı sonrası yalnız bu yayımlanmayacak testte “bin defa” kullanıldı ve ses yeniden üretildi. İnsan düzeltmesi gibi gösterilmedi. Aligned altyazıda ilk kare fade gecikmesi kaldırıldı; tarihsel Yelda fade davranışı korundu.

Marka, font, logo, 45 karelik outro ve kapanış sesi değiştirilmedi. `EpisodeComposition.tsx` değişmedi. Ortak CaptionTrack yalnız forced-alignment cue girişini ayırır; Root yeni registry kompozisyonlarını ekler. Mevcut beş referansın yeniden render'ında fark sıfır. Tarihsel StyleProof/Yelda dosyaları değiştirilmedi.

## İnsan incelemesi bekleyen noktalar

CTC'nin 20 ms adımı çözünürlüktür; her kelimenin ±33,333 ms doğruluğu garanti edilmez. Otomatik diagnostic mismatch işaretleri:

| Kelime ID (0 tabanlı) | Kelime | Başlangıç–bitiş |
| --- | --- | --- |
| 10 | Saniyeleri | 4.240–4.840 ms |
| 42 | gösteriyor. | 18.640–19.380 ms |
| 43 | Kısa | 20.280–20.580 ms |
| 58 | Bir | 27.980–28.100 ms |
| 59 | kilometre | 28.100–28.660 ms |

Bunlar kesin telaffuz hatası teşhisi değildir; greedy diagnostic ile kesin metin arasındaki fark nedeniyle inceleme ister. Bütün sesi, özellikle açılışı, ondalık sayıları, cümle duraklarını, bu sözcükleri ve son heceleri dinle. Sayıların yazıyla okunuşu ↔ ekran metni `displayMap` ile açık eşlenir. Araç eksik kelime/çakışma/enerjili boşluk tespit eder; doğal telaffuz veya bütün hecelerin doğruluğunu otomatik garanti etmez.

Yerel inceleme: **http://127.0.0.1:3033**, `npm run episode:review -- --id production-check`. Sesi gerçekten dinleyip zamanları kontrol ettikten sonra düzeltmeleri ve onayı kaydet. Onaydan sonra bayraksız render + QA aynı veriden final MP4/SRT üretir. Henüz onaylı bir SRT veya yayına hazır bölüm teslim edilmiş gibi işaretlenmedi.

Bu oturumda baştan sona insan dinlemesi ve gerçek zamanlı tam video izleme yapılmadı. Sekiz gerçek kare incelendi; otomatik bütün-kare taraması subjektif titreme/sahne anlatım değerlendirmesinin yerine geçmez. MacBook kurulumu bu oturumda test edilmedi. Wi-Fi kapatılmadı; gerçek süreçlerin ağı OS sandbox ve probe ile engellendi. Hiçbir ses dış servise gönderilmedi, video yayımlanmadı.
