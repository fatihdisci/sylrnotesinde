# Sayıların Ötesinde

Yeni bölüm görevine başlamadan önce sırasıyla `docs/DESIGN_SYSTEM.md`, `docs/ANIMATION_RULES.md`, `docs/VIDEO_STRUCTURE.md`, `docs/EPISODE_GUIDE.md` oku.

- Marka sürümü `0.1-candidate`; kullanıcı incelemesi olmadan onaylanmış v1.0 sayma.
- Yeni bölüm: `src/episodes/<id>/` altında veri + özgün TSX sahneler. İlk gerçek konu `solar-basketball`; ses belirler, süreyi eski 45 saniye hedefine sıkıştırma.
- Palet, font, logo, outro ve kapanış sesi değişiklikleri açık kullanıcı talebi gerektirir. Bölüm koduna marka kopyası koyma; `EpisodeComposition` kullan.
- `npm run check` ve ilgili render/QA kontrollerini çalıştır. Gerçek MP4 karelerini incele; yapılmayan ses/görsel kontrolünü geçmiş gösterme.
- `tests/references/` ve eşikleri kontrol geçirmek için yenileme. Marka farklarını raporla.
- Tüm hareket kare tabanlı; render sırasında dış ağ isteği, ücretli servis ve deploy yok. Varlıkları render öncesinde yerelde hazırla. Kullanıcı `fatihdisci/sylrnotesinde` reposuna commit/push yetkisi verdi; kodu ve kurulum kayıtlarını burada sürdür.
- TTS yalnız yerel. Her model ayrı ortamda; ağırlık/ortam/üretilen büyük WAV dosyalarını Git'e ekleme. Kullanıcı Supertonic 3 / M1 erkek sesini seçti. Aktif anlatıcıyı yeni açık karar olmadan değiştirme; kaldırılmış Antalia/EMA ortamlarını varsayılan kurulumda geri kurma.
- Bu klasör dışındaki projelere dokunma. Anahtarları kaydetme. Renders ve kaynak sesleri koru.
- TTS işi öncesi `tts/docs/INSTALLATION.md`, `tts/docs/PROTOCOL.md`, `tts/docs/REMOTION.md` oku. Kilit/revision/model kimliği değiştirilirse raporla; Mini ve Antalia 1’i karıştırma.
- Anlatıcı seçimi `tts/config/narrator.json` üzerinden yalnız kullanıcı kararından sonra. Mevcut StyleProof/Yelda sesleri tarihsel test varlıklarıdır; onları ve görsel/outro bileşenlerini değiştirme. Yeni bölümlerde kullanıcı tarafından verilen hazır MiniMax/harici sesi kullan. Supertonic 3 / M1 yerel yedek ve tarihsel sistem olarak korunur; açık istek olmadan yeni TTS üretme. Her iki cihazda venv’yi yerelde yeniden kur.
- Ses değişikliğinde `npm run tts:test`, `npm run tts:qa` ve gerektiğinde `npm run tts:offline`. Öznel kaliteyi veya sözcük senkronunu ölçmeden doğrulanmış sayma. Kullanıcı puanları ile TEST FIXTURE kayıtlarını ayır.

- Gerçek bölüm üretimi öncesi `docs/PRODUCTION_GUIDE.md` ve `alignment/docs/METHOD.md` oku. `episode:import-voice -- --id <id> --audio <dosya> --script <kesin-metin>` → yerel kelime incelemesi → ses temelli storyboard → `episode:sound` → `episode:render` → `episode:qa`. Eski `tts:episode` yalnız ham/tarihsel ses hazırlığıdır.
- `--draft` taslağa izin verir; bayraksız yayın komutları insan dinleme/onay kaydı ve güncel metin/ses/ayar/hizalama hash’lerini zorunlu tutar. CTC güveni insan onayı değildir; `approved` durumunu kullanıcı adına yazma.
- SRT ve gömülü altyazı aynı word-timing export’undan gelir.30 FPS başlangıcı floor, bitişi ceil; eski Yelda cue fade’i korunur. Ağırlık, venv ve büyük WAV Git dışıdır.
- Yeni özgün Scenes.tsx + production.json ve registry kaydı yeterlidir. Genel scriptlere bölüm süresi/kare listesi gömme. `episode:test`, `alignment:test`, gerçek MP4 QA ve marka referanslarını çalıştır.

- Güncel kullanıcı kararı: yeni `audio-first` videoların süresini gerçek ses belirler; 40–45 s zorunlu değildir. Ses hızlandırılmaz, sonu kesilmez; son45 kare kanonik outro. Orijinal ses `voice-sources/` içinde hash ile arşivlenir. MiniMax API/hesap entegrasyonu yok.
- Yeni üretim rehberi: `docs/AUDIO_FIRST.md`. Storyboard gerçek sözcük ID/metin çapalarından çözülür; TSX, efekt miksajı ve inceleme çıktısı aynı olay verisini kullanır. Otomatik hizalama insan dinlemesi veya yayın onayı değildir.

- 10 Ekim 2026 açık kullanıcı isteği: `solar-basketball` için Antalia-2 Mini (`antalia-mini==1.0.0`, Python 3.12, CPU) yeniden kuruldu. Yalnız `--model antalia-mini` kur; EMA’yı geri kurma, M1 ortam/ağırlık/ayarlarını değiştirme. Merkezi anlatıcı hâlâ Supertonic 3/M1. Antalia bu bölüm için `production.json.narrationSettings` + açık `episode:prepare --synthesize-model antalia-mini` ile seçilir; otomatik temizlik yapma.
- Bu bölümde kullanıcı özgün Three.js sanat yönetimi istedi: `SolarBasketball` izole wrapper’ı korunmuş font/imza/Outro bileşenlerini kullanır. `src/brand` ve `EpisodeComposition` üstüne yazma. Kaynak/haklar ve tek fiziksel ölçek için `docs/episodes/solar-basketball/` oku.
- Kalıcı kullanıcı tercihi: altyazıların hemen üstüne küçük açıklama, teknik not veya ölçek dipnotu ekleme. `solar-basketball` videosundaki bu açıklama katmanı kaldırıldı; gelecek videolarda yeniden oluşturma. Ölçek/varsayım kayıtlarını üretim belgelerinde tut.
- Ses tercihi: görsel olaylarla senkron, yumuşak tonal blink/bip sesleri kullan. Hışırtılı noise katmanlarını ve gürültülü whoosh efektlerini varsayılan ses tasarımı yapma; anlatımı koru.

- Kalıcı ses tercihi: anlatıcı miksin önüne aşırı çıkmaz; belirgin yumuşak blink/bip efektleri ve hoş, hafif ritmik müzik duyulur. Yeni bölümlerde `docs/AUDIO_STYLE.md` oku ve bu dengeyle başla; kullanıcıya her bölümde yeniden söyletme.

- Güncel açık kullanıcı isteği: Chatterbox Multilingual V3 ayrı `tts/environments/chatterbox` / `tts/models/chatterbox` içinde kuruldu. İsteğe bağlı `npm run tts:chatterbox:setup` ve `npm run tts:chatterbox` kullan; varsayılan M1 seçimini değiştirme. `solar-basketball-chatterbox-tr` yeni sesle yeniden hizalanmış ayrı adaydır; eski güneş videosu/testlerini ezme. Kurulum ve Türkçe-only çevrimdışı uyumluluk notları `tts/docs/CHATTERBOX.md` içinde.
