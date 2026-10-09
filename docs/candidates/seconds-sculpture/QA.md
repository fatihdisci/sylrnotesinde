# Zaman heykeli — teslim / QA

Son kullanıcı düzeltmesi uygulandı: altyazı üzerindeki gün kesri, birim açıklaması,1+999 ve şematik koreografi notlarının tamamı kaldırıldı. Tam master ve14sn prototip temiz yerleşimle yeniden render edildi. Önizleme de yenilendi. Kalıcı marka değişikliği/onayı yoktur.

## Gerçek çıktılar

- Tam master: `renders/episodes/seconds-sculpture/draft.mp4` —1080×1920,30FPS,H.264/AAC,1497 kare,49,9sn.
- Prototip: `renders/episodes/seconds-sculpture/prototype.mp4` —1080×1920,30FPS,420 kare,14sn. Gerçek sesin24,867–38,867sn kesiti; yeni TTS değil.
- Mobil kopya: `renders/episodes/seconds-sculpture/mobile-preview.mp4` —540×960.
-48 kontrol karesi: `controls/`, zaman haritası `control-frames.json`; üç kronolojik `contact-*.jpg`; ayrıca `clean-day.png`, `clean-result.png`, `reveal-review.jpg`.
- Otomatik kanıtlar: `qa.json`, `layout-qa.json`, `extra-qa.json`, `draft.mp4.json`.
- Ses, SRT, kelime zamanları, çözülmüş storyboard ve ayrı SFX stem'i: `public/episodes/seconds-sculpture/`.

Masterın kaynak/render hash'leri birbirini doğrular. Büyük medya Git dışıdır. Yeni kaynak, süre ve hizalama dosyaları Git'te sürümlenir. Dosya adındaki draft, insan dinleme onayının verilmediğini belirtir; master çözünürlüğü1080×1920'dir.

## Teknik sonuçlar

| Kontrol | Gerçek sonuç |
|---|---|
| Orijinal MP3 arşivi | Verilen dosyayla aynı SHA256; dosyaya yazılmadı |
| WAV süresi |47,115458sn; tempo/perde/duraklar değişmedi |
| Kelime kapsamı |87/87,18 kısa altyazı öbeği; en fazla iki satır |
| Altyazı dışa aktarımı | SRT ile gömülü altyazı aynı frame cue verisi |
| Encode ses kayması | Baş/orta/son0ms; drift0ms |
| Voice korelasyonu |0,99273 /0,99992 /0,97819; SFX miks içinde |
| Görsel olay/SFX miks kontrolü |21/21 olayda0ms; minimum korelasyon0,99882 |
| Ses efekti adedi |27; ayrı yerel orijinal stem, harici örnek yok |
| Efekt/konuşma oranı | Aktif10ms pencerelerde medyan−13,78dB; p95−6,38dB; gerçek WAV ducking |
| Son MP4 ses düzeyi |−20,94LUFS;−8,59dBTP; sample peak0,51623; clipping yok |
| Outro |1452.kare/48,4sn başlangıç;45 kare; kapanış sesi0ms, korelasyon0,99999 |
| Prototip |420 kare; gerçek ses+stem kesitiyle0ms, korelasyon0,99986 |
| Font/taşma/çakışma |103 gerçek Chromium yerleşim probu;0 ihlal/çakışma;5 yerel font yüklü |
| Bilgi notları |103 yerleşim kaydında day-measure/scale-note düğümü yok |
| Siyah/boş içerik |0; ana geometri boşluğu0 |
| Uzun sessiz+durağan |2sn üzeri aday0; neredeyse durağan aralık0 |
| Sayısal doğruluk |1e6/86400=11,574074 gün;1e9/31557600=31,688088 yıl; tam1000 eş parça |
| Geometri | Kaynak birim iki kez sayılmıyor. Çıkarılan1 ve kalan999; hepsi aynı boyda |
| Son kadraj | Geometrinin köşeleri projekte edilerek kırpılma ve altyazı boşluğu testi geçti |
| Marka regresyonu |17 korunan dosya değişmedi;5 tarihsel referansta piksel farkı0 |

Yıl365,25 gün varsayımıdır. Heykeldeki boşluklar ve perspektif,1000 kat uzunluk/ekran alanı iddiası değildir. Karşılaştırma1000 aynı boydaki parça adedi/toplam katı hacmidir. Koreografi açıklayıcı bir görsel metafordur.

## Görsel yönetmen incelemesi

İlk prototip ve ilk tam MP4'ün kontrol dizileri incelendi. Düz ızgara etkisi, aşırı yakın sonuç kamerası ve günler bölümündeki sayı/nesne yaklaşması zayıf bulundu. Derinlik katmanları buruldu; kamera başlangıcı makro yüzeye alındı; günler/sonuç kamerası açıldı; küçük parça görünür alana taşındı. Ölçek açılışındaki tek karelik nesne belirmesi yerine, nesneler mesafe/sis içinden açılıyor. Son kullanıcı isteğiyle bilgi notları tamamen silindi.

Son MP4'ün başlangıç, kapak açılması, kadran, yaprakların açılması/dolması/katlanması, kamera uzaklaşması, kilitlenme, yıl sonucu, parça çıkarılması ve outro kontrolleri çıkarıldı.12sn civarındaki saatten günlere geçiş ile26sn civarındaki ölçek açılışı ardışık karelerle incelendi.26,20–26,43sn büyük piksel değişimi8 ardışık kareyi işaretliyor: bu hızlı parallax/geri çekilme; rastgele tek karelik flaş veya boş görüntü değil. Eşik değiştirilmedi.

Gerçek MP4 yerel tarayıcıda oynatıldı; prototip ve tam filmde ilerleyen zaman, birkaç geçiş ve son kadraj ekran gözlemleri kontrol edildi. Bu, her kareyi kesintisiz insan gözüyle izleme veya insan dinleme onayı değildir. Hareket analizine bütün MP4 kareleri dâhil edildi. Adayın yaratıcı başarısının son değerlendirmesi kullanıcıya aittir; bu rapor “olağanüstü kalite onaylandı” iddiası taşımaz.

Hatırlanması hedeflenen an: aynı mercan parçanın etrafındaki derinlik koridorunun bir dev hacme kilitlenmesi ve sonra tek parçanın bu kütleden ayrılması. Nesneler ışık/gölge ve gerçek perspektif taşır. Sabit sunum başlığı kaldırıldı; büyük kavram tipografisi anlatım boyunca değişir. Dekoratif parçacık, rastgele glitch, kamera sallama veya sürekli müzik yok.

## Ses / sözcük inceleme sınırı

Gerçek WAV yeniden hizalandı;87 sözcüğün başlangıç/bitişleri önceki MiniMax içe aktarmasıyla birebir aynı çıktı. CTC20ms adımı, algısal33ms doğruluk garantisi değildir. İnsan dinleme yapılmadı; `needs_review`, `listened:false` ve yayın kapısı korunur. Aşağıdakiler yalnız greedy tanı metni uyuşmazlığıdır; kesin telaffuz/zaman hatası ilan edilmez:

| Sözcük ID | Sözcük | Gerçek hizalama aralığı | İnceleme nedeni |
|---|---|---|---|
|10|üç|5,080–5,260sn|Tanı metninde “üçsıfır” birleşmesi|
|11|sıfır|5,260–5,600sn|Aynı birleşme|
|27|dönüşüyor|15,540–16,180sn|Tanı metni “dönüşiüyor”|
|34|virgül|19,780–20,200sn|Tanı metni “virül”|
|55|Her|32,220–32,460sn|Tanı metninde “herbiri” birleşmesi|
|56|biri|32,460–32,700sn|Aynı birleşme|

Kullanıcı, kulaklık ve telefon hoparlöründe özellikle ölçek geçişlerinin gücünü, anlatıcının anlaşılmasını ve bu altı sınırı dinlemeli. Otomatik miks ölçümü duyumsal ses kalitesi onayı değildir. Kelimelere veya konuşma metnine müdahale edilmedi.

## Çalıştırılan testler

- `npm run check`:17/17 Node testi; TypeScript, ESLint, marka kontrolü geçti.
- `EPISODE_TEST_ID=seconds-film npm run episode:test`:14/14; atlanan test yok. Gerçek tarihsel M1 fixture ve harici ses bütünlük testleri.
- Yeni aday üzerinde ayrıca gerçek HTTP ses-range/geçersiz inceleme kaydı testi:1/1. Kullanıcı onayı yazılmadı; varlıklar değişmedi.
- `npm run alignment:test`:5/5.
- `npm run tts:test`:7/7.
- `npm run tts:qa -- --episodes seconds-film motion-study-15`:2 korunmuş M1 WAV'ı,0 hata;−20,13..−20,11LUFS,−2dBTP. Ses üretilmedi.
- `npm run qa:fonts`:5/5 Türkçe/sayı/ok/çarpı karakterleri.
- `npm run references:check`:5/5, tümünde piksel farkı0.
- `episode:render` ve `episode:qa --draft --gl angle`: son temiz1080 masterda geçti. Prototip de ayrıca gerçek MP4 üzerinden ölçüldü.

Sınırlama: bayraksız tarihsel `npm run tts:qa`, bu Mac'te eski Antalia Mini `A-original.wav` arşiv kopyası bulunmadığı için çalışmasını tamamlayamadı. Arşivi değiştirmek veya yeni TTS üretmek yerine, mevcut seçili M1 dosyalarıyla kapsamlı kontrol çalıştırıldı ve geçti. Kaldırılmış modeller geri kurulmadı. Three.js'in iç R3F Clock kullanımına dair deprecation uyarısı var; render hatası/kare kaybı yok. Bu uyarı kaynak animasyonlarda duvar saati kullanıldığı anlamına gelmez.
