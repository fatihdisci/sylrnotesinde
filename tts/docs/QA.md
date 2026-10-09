# Yerel TTS QA · 2026-10-09

Makine: Apple M4 Mac mini, 16 GiB RAM, 10 CPU çekirdeği, macOS 27.0 arm64. Bunlar bu makinede gerçek üretimden ölçülen değerlerdir; model kalite sıralaması değildir. İki CPU thread, seed42; süreler import/model yüklemesinden ayrı sentez süresidir. CPU %100 bir çekirdek, RSS süreç belleğidir.

## Çalışma durumu

| Model | Gerçek profil / ana WAV | Doğal D uzunluğu | A–D sentez süresi | A–D ortalama CPU aralığı | A–D tepe RSS | Native |
|---|---:|---:|---:|---:|---:|---:|
| Antalia-2 Mini · çalışıyor | 1 / 6 | 43.31 sn | 0.138–0.790 sn | 98.3–152.2 % | 527.0 MiB | 48000 Hz |
| EMA Lightning · çalışıyor | 1 / 6 | 37.76 sn | 0.283–1.388 sn | 126.3–142.3 % | 416.4 MiB | 48000 Hz |
| Supertonic 3 · çalışıyor | 10 / 60 | 40.12–49.32 sn | 1.170–8.606 sn | 136.0–200.4 % | 777.7 MiB | 44100 Hz |

6 Antalia +6 EMA +60 Supertonic =72 master. Her birinin 48 kHz mono PCM24 eşitlenmiş dinleme kopyası var. Ham dosyalar FLOAT WAV; raw peak masterda korunur.

## Uzun metin profilleri

| Model / profil | Doğal D | 42 sn varyant | Göreli hız |
|---|---:|---:|---:|
| Antalia-2 Mini / default | 43.315 sn | 42.045 sn | 1.03130 |
| EMA Lightning / default | 37.760 sn | 41.880 sn | 0.89905 |
| Supertonic 3 / M1 | 48.100 sn | 42.076 sn | 1.14523 |
| Supertonic 3 / M2 | 47.311 sn | 42.067 sn | 1.12645 |
| Supertonic 3 / M3 | 40.117 sn | 41.972 sn | 0.95517 |
| Supertonic 3 / M4 | 45.518 sn | 42.046 sn | 1.08376 |
| Supertonic 3 / M5 | 48.051 sn | 42.076 sn | 1.14407 |
| Supertonic 3 / F1 | 48.066 sn | 42.076 sn | 1.14442 |
| Supertonic 3 / F2 | 45.610 sn | 42.047 sn | 1.08596 |
| Supertonic 3 / F3 | 49.325 sn | 42.089 sn | 1.17439 |
| Supertonic 3 / F4 | 41.783 sn | 41.997 sn | 0.99482 |
| Supertonic 3 / F5 | 46.861 sn | 42.062 sn | 1.11573 |

## Ses doğrulaması

- 72/72 dosyada okunabilir/sonlu/dolu WAV, beklenen native sample rate, 48 kHz dinleme rate ve süre korunumu: **geçti**. Boş/bozuk WAV yok.
- Teslim dinleme WAV’ı yeniden ölçüldü: LUFS -20.32…-19.92; maksimum true peak -1.90 dBTP. PCM dinleme kopyasında clipping yok.
- İnternet izolasyonu: üç model bağımsız A tekrarında OS ağ yasağı + Python ağ hook’u içinde sentez yaptı; hiçbir ağ girişimi kaydedilmedi. Ayrı socket probu OS yasağını doğruladı. Üçünde ilk üretim ile decode edilmiş örnekler birebir aynı. WAV PEAK zaman damgaları nedeniyle dosya-byte hash kıyasının uygun olmadığı bulundu ve PCM kıyasıyla düzeltildi.
- Ham ve dinleme çıktılarının uzunlukları 5 ms tolerans içinde; loudnorm son sözcükleri süre kısaltarak kesmiyor. Supertonic ONNX padding her parçada ayrı kesiliyor, son parçanın başından yanlış kesme önleniyor. Son sözcüğün fonetik bütünlüğü kulakla onaylanmadı.

## CPU / MPS denemesi

| Model | MPS A sentezi | A süresi | Sonuç |
|---|---:|---:|---|
| Antalia-2 Mini | 5.871 sn | 9.699 sn | Gerçek WAV; ilk MPS koşusu CPU’dan yavaş |
| EMA Lightning | 5.289 sn | 8.960 sn | Gerçek WAV; ilk MPS koşusu CPU’dan yavaş |
| Supertonic 3 | — | — | Resmî sabit ONNX yolu CPU; MPS backend yok |

MPS ısınmış uzun koşu karşılaştırması yapılmadı. Antalia MPS’de PyTorch istft çıktı yeniden-boyutlama deprecation uyarısı verdi; WAV üretildi. Bu uyarı saklanıyor; performans/kararlılık üstünlüğü iddiası yok. CPU varsayılan kalır.

## Arayüz ve proje doğrulaması

- Gerçek tarayıcı: Türkçe metin/font yükleme, küçük ekran ve üç sütunlu masaüstü yerleşimi incelendi; DOM’da yatay taşma yok. İlk doğal A WAV ve uzun D 42 sn WAV oynatma kontrolü; uzun örnekte ilerleyen currentTime ve gerçek 42,045 sn duration, error=null görüldü. Oynat/duraklat/durdur, profil F5 geçişi, D42 varyantı çalıştı.
- Ayrı 3031 TEST FIXTURE oturumunda 12 örnek ×4 ölçüt ve yorumlar kaydedildi; sayfa yeniden açıldığında 12/12 korundu; isim açma düğmesi çalıştı. Gerçek 3030 kullanıcı oturumu 0/12 ve isimler kapalı olarak bırakıldı. Test puanları kalite sonucu değildir.
- Backend testleri: puan sınırı/türü, yanlış kimlik/çok uzun yorum reddi, erken isim açmayı engelleme, JSON kalıcılığı, HTTP Origin/Host reddi, anonim ses byte-range yanıtı, path traversal reddi ve 12 profil/72 dosya bütünlüğü.
- Yerel kurulum yeniden çalıştı: sabit iki Python sürümü, üç ayrı bağımlılık kilidi, 29 varlık. MacBook’ta doğrudan çalıştırma bu Mac mini oturumundan yapılmadı. Taşınabilir komut akışı bu Mac’te denendi.
- `npm run check`: TypeScript, ESLint, mevcut4 test ve 17 marka dosyası hash kontrolü geçti. Beş gerçek referans render’ı (opening, hundred, result, outro, board) karşılaştırıldı: tümünde meanError=0 ve changedRatio=0. Referans kare eşiği veya dosyası yenilenmedi. Görsel/animasyon/outro kaynakları değiştirilmedi.
- Bölüm hazırlama gerçek Antalia D sesiyle 43,315 sn /1345 toplam kare manifest üretti. İlk taslak altyazılar boş ve inceleme bayrağı açık. Build-time loader bu inceleme tamamlanmadan kullanımı reddeder.

## Yapılmayan incelemeler

Sesleri kulakla dinleyip telaffuz/doğallık/nefes/tonlama puanlamadım. Dinleme arayüzünün çaldığını teknik olarak doğruladım; bu öznel kalite onayı değildir. Sözcük zamanları insan tarafından doğrulanmadı. Yeni anlatımlı Remotion bölüm render’ı ve onun ağız/altyazı senkron incelemesi yapılmadı; ilk gerçek bölüm konusu hâlâ bekleniyor. Model kazananı seçilmedi, hiçbir model/ortam/ağırlık silinmedi.

Ham ölçüm kayıtları: `config/catalog.json`, `config/audio-qa.json`, `config/offline-test.json`, `config/mps-test.json`. Her WAV yanında ayrı metadata JSON bulunur. Loglar büyük yerel çıktılarla birlikte Git dışı `tts/outputs/` altında.
