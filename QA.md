# QA — 9 Ekim 2026

**Durum: 0.1-candidate. Kullanıcı tasarım onayı bekleniyor; v1.0 değildir.** İlk gerçek bölüm üretilmedi.

| Kontrol | Sonuç / kanıt |
|---|---|
| TypeScript, ESLint, temel testler | Geçti. 4 test grubu; 405 içerik karesinin tamamında sayaç/görünür nesne ve kırpılma kontrolü |
| MP4 formatı | İkisi de H.264/yuv420p,1080×1920,30 FPS |
| Süre/kare | StyleProof15,000 s/450 kare; Outro1,500 s/45 kare. ffprobe ile sayıldı |
| Birim doğruluğu | 1.000 benzersiz konum;100'er birimlik10 blok. f0–89:10; f144–209:100; f270–404:1.000. Ara sayaçlar çizilen tam adet |
| Fontlar | Beş WOFF2 dosyası yerelde yüklendi. Sans400/500/600,Mono400/500. Türkçe ve×/→ glyph cmap kontrolü geçti |
| Güvenli alan/taşma | Sekiz gerçek Chromium yerleşiminde sınır/scrollWidth kontrolü geçti |
| Metin çakışması | İlk kontrolde sayaç satır kutusu ile yardımcı etiket çakıştı. Sayının line-height değeri düzeltilip tekrar render edildi; son kontrolde çakışma yok |
| Görsel inceleme | MP4'ten15 kare çıkarıldı ve kontak sayfası incelendi. Ayrıca f24,108,228,270,360,429 tam boy incelendi; son düzeltmeden sonra güncel kontak sayfası ve sonuç/outro tekrar kontrol edildi |
| Boş/siyah kare | İki MP4'ün toplam495 karesi decode edildi. Çeyrek boyda her karede en az105 zemin dışı piksel; tamamen boş kare yok |
| Geçiş/tutma | En büyük fark f405'te beklenen outro kesmesi. Sonuç tutuşunda ortalama piksel farkı en fazla0,0434/255; kodlanmış görüntü sabit. Kare örneklerinde istenmeyen flaş görünmedi |
| Ses clipping/bitiş | AAC decode mono ölçümünde StyleProof peak−5,90 dBFS;Outro−9,15 dBFS. Son120 ms sessiz. Ani ses kesilmesi/taşması ölçümlerde yok |
| Ses başlangıcı | Outro olayları beklenen0,0667/0,3333/0,7333 s; decode aktif başlangıçları0,06675/0,33342/0,73367 s |
| Ortak motif | StyleProof içindeki ve ayrı Outro MP4'ündeki decode ses korelasyonu0,99998 |
| Son cümle | Aktif konuşma12,7295 s'de biter;outro13,5 s'de başlar. Ses dosyası da12,929 s civarında tamamlanır |
| Marka koruması |17 korumalı dosyanın SHA-256 kontrolü geçti. İlk kez kaydedilen5 aday referansın yeniden render karşılaştırması sıfır piksel farkıyla geçti |
| Yerel önizleme | localhost:3020/StyleProof açıldı;450 kare/1080×1920/30 FPS ve hata katmanı=null doğrulandı. f360'a seek çalıştı |

İnceleme dosyaları: `renders/qa/frame-*.png`, `contact-sheet.png`, `layout-report.json`, `font-coverage.json`, `media-report.json`, `reference-report.json`. Güvenli alan örneği `renders/safe-area-debug.png`. Piksel regresyon referansları `tests/references/` içinde; MP4 karelerinden ayrı, kayıpsız still çıktılarıdır.

**İnceleme sınırları:** Ses bu oturumda dinlenerek değerlendirilmedi. Yelda'nın doğallığı, vurgu/ton ve öznel efekt dengesi onaylanmış sayılmaz. Anlatım yerel ve geçicidir. Sözcük zamanları doğrulanmadı; dosya/cümle süreleri ölçüldü, altyazılar sahne öbekleridir. Sürekli oynatımın algısal akıcılığı için insan incelemesi gerekir; kare örnekleri, tüm karelerin decode analizi ve deterministik kamera testleri bunun yerine kusursuz akıcılık iddiası taşımaz.

AAC örnekleme blokları nedeniyle ses stream'inde yaklaşık15,019/1,515 s kodlayıcı dolgu bulunabilir. Son örnekler sessizdir; MP4 video süresi ve kare sayısı tam15/1,5 s'dir.

Küçük uygulama kararları: ana kamera54/60 kare; onluk bloklar5×2 düzende; bir kare bir birim, gruplama örnekleme değildir. Font/ses hazırlığı render'dan ayrı tutuldu. Küçük marka imzası ortak bölüm zarfına alındı; bölüm başına konum/boyut değiştirilmez. Renk/font/outro referansları kullanıcı talebi olmadan güncellenmez.
