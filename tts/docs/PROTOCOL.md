# Dinleme protokolü

Model seçimi ve öznel kalite puanları kullanıcıya aittir. Altyapı hiçbir adayı kazanan ilan etmez; aktif anlatıcı null kalır. Model/venv/ağırlık silme komutu eklenmedi.

A, B ve C metinleri kullanıcının verdiği Unicode Türkçe metin ve noktalama ile aynen `test-texts/tests.json` içinde. D, 93 kelimelik özgün ışık yolculuğu anlatımıdır. Bilim dayanakları: [NASA, ışık yılı](https://science.nasa.gov/exoplanets/what-is-a-light-year/), [NASA, Ay ışığının 1,3 saniyelik yolculuğu](https://science.nasa.gov/mission/webb/science-overview/science-explainers/how-does-webb-see-back-in-time/), [NASA, geçmişi gözlemek](https://science.nasa.gov/mission/hubble/science/science-behind-the-discoveries/time-travel-observing-cosmic-history/). Erişim 2026-10-09. C’deki kâğıt cümlesi kullanıcı test metnidir; yayımlanacak bölümün fiziksel varsayımlarını doğrulanmış saymaz. Katlama idealizasyonu, başlangıç kalınlığı ve fiziksel uygulanabilirlik gerçek bölümde ayrıca ele alınmalı.

Her profil için altı örnek:
1. A doğal anlatım, orijinal hız.
2. B sayılar/ölçüler, orijinal yazım.
3. B-normalized: aynı sayılar Türkçe yazıyla; ayrı tanı örneği. Orijinalin yanlış okunduğu varsayılmadı. Dinleyici karşılaştırır.
4. C açılış, orijinal yazım.
5. D uzun anlatım, doğal hız. Aynı metin doğal hızda her modelde 40–45 saniyeye sığmaz; gerçek süre gösterilir.
6. D-duration-42: doğal D uzunluğu / 42 çarpanıyla model içi hız değiştirilerek ikinci sentez. Metin/noktalama aynı, ses zaman esnetmesi yok. Sonuçlar 41,88–42,09 saniye.

12 gerçek profil × 6 = **72 ana WAV + 72 dinleme WAV**. Antalia ve EMA birer profil, Supertonic M1–M5 ve F1–F5. Diğer modellerde olmayan profiller taklit edilmedi. `speed=1` Antalia 0,95 / EMA 1 / Supertonic 1,05 yerel parametrelerine karşılık gelir. Bu önerilen doğal hız protokolüdür; eşit dakika başı sözcük iddiası yok. Seed 42, iki CPU iş parçacığı. Antalia’nın resmî varsayılan EQ/normalizer/okuma düzeltmeleri korunur. EMA varsayılan sentez, CPU batch=1, CUDA Lightning kapalı. Supertonic 8 adım, tr, parça arası 0,3 saniye.

Ham çıktı mono IEEE FLOAT WAV, modelin doğal hızı ve örnekleme frekansı: Antalia/EMA 48 kHz, Supertonic 44,1 kHz. Float master modelin olası 1’i aşan örneklerini kırpmadan saklar. Dinleme kopyaları ffmpeg iki geçişli loudnorm: −20 LUFS, −2 dBTP hedefi, LRA11, 48 kHz mono PCM24. Master değişmez. Dinamik eşitleme nefes/ritim yorumunu etkileyebilir; tüm adaylarda aynı işlem, ham sesler ayrıca mevcut. Dosya başına ölçümler catalog ve audio-qa içinde.

## Körlük ve kayıt

Yerel sunucu model sırasını rastgele bir kez belirler; adlar Model A/B/C, profiller Ses1… şeklindedir. Eşleme Git dışı private-session.json içinde; tarayıcıya isim veya model içeren ses URL’si verilmez. Dosyalar anonim kimlikle servis edilir. Profil sayısı veya tanıdık tını modeli tahmin ettirebilir; bu sınırlı tek kör dinleme, çift kör bilimsel çalışma iddiası değildir.

İlk ses profilinde dört testi üç model için dört ölçütte tamamlayınca 12/12 olur ve isim açma düğmesi etkinleşir. Ek ses profilleri ve ek varyantlar isteğe bağlıdır. İsimleri açmak model seçmek değildir. Her puan/not değişikliği yerel JSON’a yazılır; kısmi puanlar da korunur. “Sonuçları JSON indir” yedek alır. İsimler açıldıktan sonra dışa aktarılan dosyada gerçek kimlikler bulunur. Hiçbir puan otomatik kazanım veya kalite iddiası oluşturmaz.

Aynı anda tek ses oynar; sırayla dinle A/B/C adaylarını seçili profil/varyantla oynatır, “Tümünü durdur” kuyruğu da iptal eder. Başka teste/profil türüne geçmek çalmayı durdurur. Sunucu yalnız 127.0.0.1, Host/Origin kontrolü ve self-only CSP kullanır; fontlar dahil tüm varlıklar yereldir. CDN, analitik veya ses yükleme yok.

## Teknik ölçüm sınırları

Worker wall-clock süresi, model yükleme süresi, süreç CPU saniyesi, ortalama CPU yüzdesi (100 = bir tam çekirdek; çok çekirdekte 100’ü aşar), 20 ms aralıkla süreç RSS tepe değeri ve gerçek WAV uzunluğu kaydedilir. Yükleme sonrası sentez süreleri ile ilk import/yükleme ayrı. Tek makinede birer koşu, istatistiksel performans testi değil. RSS, GPU belleğini veya tüm sistem RAM’ini ölçmez. Ölçüm anındaki başka işler sonucu etkileyebilir.

Tüm corpus üretimi macOS sandbox-exec `deny network*` içinde, ayrıca Python socket audit hook ve HF offline bayraklarıyla yapıldı. Sonradan bağımsız A tekrarları üç adayda aynı decoded PCM SHA256’yı verdi. OS sandbox’ın bağlantıyı reddettiği ayrı socket probuyla doğrulandı. Mac’in Wi-Fi/Ethernet bağlantısı kapatılmadı; yalnız süreç çevrimdışıydı. FLOAT WAV PEAK başlığı libsndfile zaman damgası içerir; dosya SHA256 değişebilir, deterministik karşılaştırma decode edilmiş float PCM üzerinden yapılır.

WAV geçerliliği, sample rate, süre, sayısal sonluluk, RMS, LUFS ve true peak ölçüldü. Arayüzde oynatma ilerlemesi, durdurma, profil/varyant değişimi, puan/not kalıcılığı ve isim açma ayrı TEST FIXTURE oturumunda denendi. Test puanları kullanıcı oturumuna yazılmadı. Telaffuz, doğallık, son sözcüğün eksiksizliği, nefes hissi ve uzun anlatım dinlenebilirliği **kulakla değerlendirilmiş sayılmıyor**; kullanıcı dinlemesi bekleniyor. EMA word timing kayıtları modelin 40 ms ızgarasından gelir ve insan doğrulamasından geçmedi.
