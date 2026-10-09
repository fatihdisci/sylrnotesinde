# MacBook yerel üretim kaydı · 2026-10-09

Cihaz Apple M5, arm64/macOS. Main49c3505 ile başlandı; temiz çalışma alanı ve origin/main ile eşitlik doğrulandı. Başka projeye veya sistem Python'una paket kurulmadı.

- `npm ci`:347 paket,0 bildirilen güvenlik açığı. Host Node24.16.0 sürümü repo engine'inden farklıydı; üretim/typecheck/lint/test/render/reference komutları için Node22.22.3 resmî dağıtımı proje içi `.cache/runtime/` altında hazırlandı.
- `npm run browser:prepare`: yerel Chrome Headless Shell157.0.8080.0.
- `npm run tts:setup`: yalnız Supertonic3; CPython3.11.15, ONNX Runtime1.23.1, sabit mevcut kilit ve19 yerel varlık doğrulandı. Antalia/EMA kurulmadı.
- `npm run alignment:setup`: ayrı CTC venv, PyTorch2.8.0 / Transformers4.57.6 / NumPy2.2.6 ve sabit revision708639f50559d7970f462e13ec64d3f059ca89f6. Tüm model dosyaları SHA256 ile doğrulandı. İlk indirme sırasında çakışan iki kurulum denemesi dosya hatası verdi; tek süreçle tekrar doğrulama başarılı oldu.
- FFmpeg/ffprobe cihazda zaten mevcuttu.
- Font QA için proje `.venv` ortamı: fonttools4.62.1 / brotli1.2.0. Beş fontun Türkçe ve sayı glyph testi geçti.
- Anlatıcı/config/model revision/kilit/seed/hız değiştirilmedi. Büyük WAV, model, venv ve yeni MP4'ler Git dışıdır.

TTS çevrimdışı bağımsız tekrarında decoded PCM birebir aynı; OS socket probu erişimi reddetti. 15 saniyelik çalışmanın29 ve tam videonun87 kelimesi çevrimdışı tekrar hizalamasında birebir aynı zamanı verdi. Ham kayıtlar `tts/outputs/episodes/`, dinleme WAV'ları `public/episodes/`, render'lar `renders/episodes/` altında korunur.

Üretim ortamları cihazlar arasında kopyalanmaz. Aynı paket/model sürümü farklı donanımda bit eşitliğini garanti etmez; bu M5 üzerindeki tekrar testi yalnız bu cihaz için kanıttır.
