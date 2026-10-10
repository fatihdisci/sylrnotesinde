# Güneş Bir Basketbol Topu Olsaydı? — QA

10 Ekim 2026 · `0.1-candidate` · **Tam kalite inceleme filmi. İnsan ses/kelime onayı verilmedi; yayın onayı yok.**

Teslim: `deliveries/solar-basketball/gunes-basketbol.mp4`. Yerel render masterıyla byte-for-byte aynıdır. H.264/AAC, 1080×1920, 30 FPS, **1.979 kare / 65,967 s**. Anlatım 63,403 s; son sözcük 63,260 s; outro 64,467 s’de başlar. Sonuç tutuşu 36 kare, outro 45 kare. Konuşma kesilmedi veya zaman esnetmesiyle hızlandırılmadı. Doğal göreli hız 1 korundu; süre sınırı olmadığı için 1,05 testi gerekmedi.

## Kullanıcı düzeltmesi — temiz tonal sesler ve sade altyazı alanı

Altyazının hemen üstündeki küçük açıklama katmanı bütünüyle kaldırıldı; 135 yerleşim probunda bu düğüm bulunmuyor. Tercih AGENTS.md ve tasarım rehberine kaydedildi.

Hışırtı üreten bütün noise/whoosh katmanları, hem efektlerden hem ambientten kaldırıldı. Görsel olaylarla aynı başlangıç karelerinde yumuşak blink/bip, kısa uyumlu nota dizileri ve düşük seviyeli sinüs pad kullanılıyor. Atak/sönümler yumuşak; konuşma sırasında efekt oranının yüzde 95 değeri −12,04 dB. Anlatıcı WAV hash’i değişmedi; kanonik outro korunuyor. [Tonal ses kontrolü](tonal-audio-check.json).

Bu düzeltmede TypeScript/lint, 21 TS testi, marka kontrolü, üretim testleri (16 geçti / 1 tarihsel fixture atlandı), gerçek MP4 render ve genel bölüm QA yeniden çalıştırıldı. Güncel MP4 ölçümleri aşağıdaki tabloda. İşitsel insan incelemesi yapılmış sayılmadı.

## Gerçek ses ve çevrimdışı çalışma

Antalia-2 Mini 1.0.0, tek erkek/default, Python 3.12.12, Apple Silicon CPU, 2 thread, seed42. Sabit model revision ve bağımlılık kilitleri değişmedi. Yalnız `npm run tts:setup -- --model antalia-mini` çalıştırıldı; Supertonic kurulumu yeniden çalıştırılmadı, EMA kurulmadı.

- Kısa Türkçe test: gerçek 48 kHz WAV, 8,355 s; üretim 0,641 s; peak RSS 368,8 MiB.
- Tam metin: gerçek 48 kHz WAV, 144 normalleştirilmiş kelime; üretim 1,357 s; model yükleme 0,405 s; CPU 1,948 s / ortalama %143,5; peak RSS 488,1 MiB. Bunlar ölçülen süreç değerleridir, başka cihaz için hız garantisi değildir.
- Tam metin macOS `sandbox-exec deny network*` altında tekrar üretildi. Ağ probu gerçekten reddedildi; networkAttempts boş; decode edilmiş bütün ses örneklerinin SHA256’sı aynı. Arayüzler kapatılmadı; süreç seviyesinde dış ağ engellendi. [Kayıt](offline-tts.json).
- Mevcut yerel `mpoyraz/wav2vec2-xls-r-300m-cv7-turkish` + CTC Viterbi ile kesin metin/WAV hizalandı. Sıfırdan bir transkripsiyonla senaryo değiştirilmedi. Aynı ses çevrimdışı yeniden hizalandı, bütün word-timing kayıtları aynı; 8,028 s / 2.571,8 MiB peak RSS. [Kayıt](../../../alignment/docs/solar-basketball-offline-qa.json).
- Supertonic ağırlıkları, bütün profiller, ortam metadata’sı, global M1 seçimi/ayarları dahil denetlenen **47 dosyanın hash’i değişmedi**. Bu kontrol ortamın her byte’ının ayrı envanteri değildir. [Envanter](supertonic-preservation.json).

Ham WAV: `tts/outputs/episodes/solar-basketball/narration.wav`. Normalize edilmiş bölüm WAV’ı: `public/episodes/solar-basketball/narration.wav`. Orijinal senaryo, sayıları yazıyla okutan script, gerçek model normalizer çıktısı ve generation ayarları bölüm dosyalarında saklıdır. Üretilmiş büyük WAV/model/venv dosyaları Git’e eklenmedi.

## Çalıştırılan kontroller

| Kontrol | Sonuç |
|---|---|
| TypeScript, ESLint | Geçti |
| TS temel/ölçek/kamera testleri | 21/21 geçti; erken ayrılan makro kamera hedefi için regresyon testi dahil |
| Üretim Python testleri | 17 test: 16 geçti, 1 atlandı; `seconds-audio-first` tarihsel dış ses/SFX dosyaları bu Mac’te olmadığı için o entegrasyon fixture’ı çalışmadı |
| TTS testleri | 7/7 geçti |
| Hizalama testleri | 5/5 geçti |
| Yeni Antalia WAV QA | 1/1 geçti; −20,05 LUFS, −1,99 dBTP, 48 kHz, son 20 ms RMS 0,000853 |
| Tarihsel dinleme WAV arşivi | 72/72 geçti; önceki rapor byte-for-byte korundu |
| Marka hash kontrolü | Korunan 17 dosyada değişiklik yok |
| Beş marka referans karesi | Hepsinde ortalama hata 0, değişen piksel 0; referans/eşik yenilenmedi |
| Gerçek render / genel bölüm QA komutları | Çalıştırıldı ve teknik kontroller geçti |
| Gerçek MP4 çözünürlük/FPS/kare | 1080×1920 / 30 / 1.979 |
| Font / güvenli alan / çakışma | 135 kare probu; beş IBM Plex dosyası yüklü, 0 taşma, 0 etiket çakışması; altyazı en fazla iki satır |
| Gerçek MP4 ses ölçümü | −21,04 LUFS, −5,78 dBTP; clipping yok |
| MP4 konuşma kayması | Başlangıç/orta/sonda 0 ms; pencerelerde korelasyon ≥0,99993; drift 0 ms |
| Efekt + müzik + anlatım | Aynı kaynak katmanlarla 22 olayda MP4 miks karşılaştırması; en düşük korelasyon 0,99992; değişmeyen >0,98 eşiği geçti |
| Outro | Başlangıç kare 1.934; ses farkı 0,313 ms, korelasyon 0,999993; konuşma ve altyazı outroyla çakışmıyor |
| SRT / gömülü altyazı | Aynı 144 kelimeden 32 öbek; aynı floor/ceil 30 FPS sınırları |
| Tüm kare taraması | 0 siyah interval, 0 boş içerik karesi; ≥2 s sessiz/durağan interval bulunmadı |
| İnceleme sunucusu | `127.0.0.1:3035/state` ve gerçek WAV byte-range yanıtı çalıştı; onay kaydı gönderilmedi |

Miks kontrolünde bilinen ses tasarımı katmanları çıkarılarak anlatıcı kayması ayrıca ölçülür; bunun yanında bütün miks bağımsız olarak her storyboard olayında karşılaştırılır. Böylece belirgin efektler yüzünden korelasyon eşiğini düşürmek gerekmedi. [Otomatik ayrıntılar](technical-qa.json).

## Görsel inceleme ve düzeltilen sorunlar

Güncel açıklamasız görüntüden 16 ana kare ve altı diagnostic kare çıkarılıp görüntü olarak incelendi. Son ses revizyonunun kodlanmış görüntü akışı bu incelenen açıklamasız renderla byte-for-byte aynıdır. Altyazısız kontrol kareleri aynı sahne/kareyle ayrıca render edildi. [İnceleme kaydı](review-record.json), [temas sayfası](../../../deliveries/solar-basketball/review-contact.jpg); bütün tam çözünürlüklü kareler `renders/episodes/solar-basketball/review/` içinde.

İlk taslakta asenkron doku yüklenmesi beklenmiyordu; render geciktirme ve GL commit bariyeri eklendi. Dünya makrosu yazıyla çakışacak kadar büyüktü; fiziksel kamera geri alındı. Geniş planda uçlar kırpılıyor ve Güneş/Dünya etiketleri çakışıyordu; tam rotayı kapsayan kamera ve ayrı lider çizgileriyle düzeltildi. Dünya’dan geri çekilirken hedef erken kayıp nesneyi kadraj dışına çıkarıyordu; hedef uzaklaşma tamamlanana kadar Dünya’da tutuldu, gerçek çıktı yeniden incelendi. Son kamera süzülmesi güçlendirildi; durağan interval uyarısı son çıktıda kalmadı. Son render bunların hepsini içerir.

Dört büyük kare farkı (322, 1.106, 1.257, 1.377) kasıtlı yakın plan / sokak kesmeleridir; ilk sürümde öncesi, kesme karesi ve sonrası gerçek MP4’ten incelendi. Geometri algılayıcısı ayrıca **124 kareyi** çok küçük/karanlık geometri diye işaretledi: milimetrelik cisimlerin geri çekilmesi, Dünya–Ay ortak ölçeği ve kuş bakışına geçiş. Eşikler değiştirilmedi. Altı aralığın temsilci kareleri incelendi; bunlar literal boş/siyah kare değildir. Özellikle küçücük cisimlerin telefonda algılanabilirliği tam ekran oynatma sırasında ayrıca değerlendirilmeli.

## Açık kalan insan incelemesi

**Bu çalışma sırasında sesi işitsel olarak dinleyemedim.** Kelime zamanları gerçek WAV/CTC’den ve sinyal ölçümlerinden gelir; fonetik doğruluk, ton/doğallık ve subjektif efekt dengesi dinlenerek onaylanmış değildir. Baştan sona insan oynatma/dinleme yapılmış gibi raporlanmadı.

24 kelime düşük güven, kısa kelime veya greedy CTC/metin farkı nedeniyle işaretli. Bunlar 24 kesin telaffuz hatası anlamına gelmez; tanıyıcının hatası da olabilir. “küçültseydik”, “milimetreyi”, “altı metre”, “santimetrelik”, kısa “o” ve “Uzay” gibi noktalar [review-record.json](review-record.json) içindeki zamanlarda görülür. Başlangıç/son heceler, bütün sayılar/birimler, “yarım milimetre” ifadesi ve iki son cümle özellikle dinlenmeli. Şüpheli zamanları tahmine göre düzeltmedim veya insan adına onaylamadım.

Mevcut yerel editör: `http://127.0.0.1:3035`. WAV’ı dinleme, konuşma/ekran metni eşlemesi, kelimeye gitme, ±1 kare ve kaydetme çalışır. Otomatik hizalama 20 ms stride kullanır; her kelimede 33,3 ms doğruluk garanti edilmez. Yayın kontrolü bu nedenle `needs_review` durumunda kalır. Tam kalite film teslim edilmiştir; yayına hazır/onaylanmış diye işaretlenmemiştir.

Kaynak, lisans ve matematik: [SOURCES_AND_LICENSES.md](SOURCES_AND_LICENSES.md). Yeniden üretim: [REPRODUCE.md](REPRODUCE.md). Hiçbir video sosyal platformda yayımlanmadı.
