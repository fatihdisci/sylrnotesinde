# Yeni bölüm üretimi

1. Tasarım, animasyon ve video yapısı belgelerini oku. Kullanıcının gerçek bölüm konusunu al. StyleProof'u yayımlanacak bölüm sayma.
2. Uzun ömürlü, doğrulanabilir bir ilişki seç. Birim ve uzunluk/alan/hacim ayrımını açıkla. Kaynakların iddiayı doğrudan desteklediğini kontrol et ve erişim tarihini kaydet.
3. `src/episodes/<id>/episode.ts` oluştur. `Episode` türü: id,title,hook,narration,sources,scenes,audio,subtitlePath,captions,brandVersion,kind,durationInFrames. `brandVersion` şu anda0.1-candidate. Kaynak veriyi yapılandırılmış tut; sahneyi dev JSON motoruna dönüştürme.
4. Anlatımı önce üret/ithal et. Varlıklar `public/episodes/<id>/` içinde. Yeni bölümlerin sağlayıcı/ses/hız kaynağı `tts/config/narrator.json` (Supertonic 3 / M1); `npm run tts:episode -- --id <id> --text-file <anlatim.txt>` ile render öncesi üret. `src/episodes/narrator.config.ts` yalnız tarihsel StyleProof/Yelda hazırlığını tanımlar; gizli anahtar ortam değişkeni. Ses sürelerini ffprobe ile ölç, cümle başlangıçlarını doğrula; istenirse sözcük hizasını ayrıca incele. Otomatik kelime senkronu varsayma.
5. `Scenes.tsx` içinde bölüme özel SVG/Canvas animasyonlarını yaz. Ortak NumberDisplay/Counter, MeasurementLine, ScaleStage, ComparisonScene, CaptionTrack, BrandMark kullanımı serbest; olayın görsel fikri bölüme özgü olsun.
6. `<EpisodeComposition episode={episode}><Scenes /></EpisodeComposition>` ile sar. Root.tsx'e composition ekle. Toplam1200–1350 kare, içerik son45 kareden önce biter. Sahne aralıkları ardışık ve bitişler hariçtir.
7. `npm run check`, `qa:fonts`, `qa:layout` ve `references:check` çalıştır. Layout scriptindeki kompozisyon/kare listesini yeni bölüm için genişlet. `qa-media.py` StyleProof/Outro kabul ölçümleridir; yeni bölümün beklenen toplam karesini ayrı kayıtla ekle.
8. `npx remotion render src/index.ts <CompositionId> renders/<id>.mp4` ile render et. Açılış, geçiş, yoğun sahne, sonuç ve outrodan en az altı gerçek MP4 karesi çıkar; metin/çakışma/güvenli alanı görsel incele. Ses başlangıç/bitiş/peak ve kuyrukları ölç, mümkünse dinle. Yapılmayan kontrolü QA'da açık yaz.

Örnek dosyalar `src/episodes/style-proof/` altında tamamen çalışan sahnelerdir. Aynı yerleşimi her bölümde kopyalamak zorunlu değildir; ortak marka davranışı korunur.

Marka koruması: `brand:check` kaynak/font/ses SHA-256 farklarını listeler. `references:check` beş kaydedilmiş PNG'ye karşı sabit toleransla yeniden render karşılaştırır ve başarısızlıkta diff üretir. Bunlar ilk adayın regresyon referanslarıdır, kullanıcı tasarım onayı değildir. Kontrol geçsin diye hash/reference/tolerans değiştirme. Yeni bölüm mevcut referansları değiştirmez.
