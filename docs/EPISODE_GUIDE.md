# Yeni bölüm üretimi

1. Tasarım, animasyon ve video yapısı belgelerini oku. Kullanıcının gerçek bölüm konusunu al. StyleProof'u yayımlanacak bölüm sayma.
2. Uzun ömürlü, doğrulanabilir bir ilişki seç. Birim ve uzunluk/alan/hacim ayrımını açıkla. Kaynakların iddiayı doğrudan desteklediğini kontrol et ve erişim tarihini kaydet.
3. `src/episodes/<id>/production.json` oluştur: başlık/hook, konuşma ve ekran metnini eşleyen öbekler, kaynaklar, hesaplanabilir iddialar, varsayımlar ve gösterim ölçeği. Örnek: `src/episodes/production-check/production.json`. `Episode` manifesti hazırlık/export adımında üretilir; marka sürümü `0.1-candidate` kalır.
4. `npm run episode:prepare -- --id <id>` ile önce seçili Supertonic 3 / M1 sesini üret, sonra ayrı yerel ortamda bilinen metni gerçek WAV'a hizala. `episode:review` ile sözcükleri dinleyip düzelt; açık insan onayı ver. JSON geçerliliği veya model skoru onay değildir. `src/episodes/narrator.config.ts` yalnız tarihsel StyleProof/Yelda hazırlığıdır.
5. `Scenes.tsx` içinde bölüme özel SVG/Canvas animasyonlarını yaz. Ortak NumberDisplay/Counter, MeasurementLine, ScaleStage, ComparisonScene, CaptionTrack, BrandMark kullanımı serbest; olayın görsel fikri bölüme özgü olsun.
6. `<EpisodeComposition episode={episode}><Scenes /></EpisodeComposition>` ile sar. `src/episodes/registry.ts` kaydı Root'a otomatik composition ekler. Toplam 1200–1350 kare; son 45 kare kanonik outro. Sahne aralıkları ardışık ve bitişler hariçtir. Kamera geometriye, okunabilir etiketler ayrı ekran katmanına uygulanır.
7. `npm run check`, `episode:test`, `alignment:test`, `qa:fonts` ve `references:check` çalıştır. Genel scriptlere bölüm kareleri/süresi ekleme; StyleProof'a özel tarihsel kontrolleri koru.
8. `npm run episode:render -- --id <id>` ve `npm run episode:qa -- --id <id>` yayın onayını ve varlık hash'lerini denetler. İnceleme öncesinde her ikisinde `--draft` kullanılabilir. QA gerçek MP4 sesini decode eder ve kontrol kareleri çıkarır. Gerçek kareleri ve sesi incele; yapılmayan insan dinlemesini veya öznel görsel kontrolü başarılı yazma.

Örnek dosyalar `src/episodes/style-proof/` altında tamamen çalışan sahnelerdir. Aynı yerleşimi her bölümde kopyalamak zorunlu değildir; ortak marka davranışı korunur.

Marka koruması: `brand:check` kaynak/font/ses SHA-256 farklarını listeler. `references:check` beş kaydedilmiş PNG'ye karşı sabit toleransla yeniden render karşılaştırır ve başarısızlıkta diff üretir. Bunlar ilk adayın regresyon referanslarıdır, kullanıcı tasarım onayı değildir. Kontrol geçsin diye hash/reference/tolerans değiştirme. Yeni bölüm mevcut referansları değiştirmez.

Gerçek üretimde `PRODUCTION_GUIDE.md` ek olarak zorunludur. StyleProof’a özel QA scriptlerine bölüm kareleri eklemek yerine genel kelime hizalama / `episode:render/qa` akışını kullan.
