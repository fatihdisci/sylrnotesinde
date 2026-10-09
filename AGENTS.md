# Sayıların Ötesinde

Yeni bölüm görevine başlamadan önce sırasıyla `docs/DESIGN_SYSTEM.md`, `docs/ANIMATION_RULES.md`, `docs/VIDEO_STRUCTURE.md`, `docs/EPISODE_GUIDE.md` oku.

- Marka sürümü `0.1-candidate`; kullanıcı incelemesi olmadan onaylanmış v1.0 sayma.
- Yeni bölüm: `src/episodes/<id>/` altında veri + özgün TSX sahneler. İlk gerçek bölüm henüz istenmedi.
- Palet, font, logo, outro ve kapanış sesi değişiklikleri açık kullanıcı talebi gerektirir. Bölüm koduna marka kopyası koyma; `EpisodeComposition` kullan.
- `npm run check` ve ilgili render/QA kontrollerini çalıştır. Gerçek MP4 karelerini incele; yapılmayan ses/görsel kontrolünü geçmiş gösterme.
- `tests/references/` ve eşikleri kontrol geçirmek için yenileme. Marka farklarını raporla.
- Tüm hareket kare tabanlı; render sırasında dış ağ isteği, ücretli servis ve deploy yok. Varlıkları render öncesinde yerelde hazırla. Kullanıcı `fatihdisci/sylrnotesinde` reposuna commit/push yetkisi verdi; kodu ve kurulum kayıtlarını burada sürdür.
- TTS yalnız yerel. Her model ayrı ortamda; ağırlık/ortam/üretilen büyük WAV dosyalarını Git'e ekleme. Model seçme veya silme; bunlar kullanıcının sonraki açık kararını bekler.
- Bu klasör dışındaki projelere dokunma. Anahtarları kaydetme. Renders ve kaynak sesleri koru.
