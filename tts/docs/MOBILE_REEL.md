# 12 profil · mobil dinleme videosu

Kullanıcının isteği üzerine tüm profillere aynı kısa cümle yeniden, tamamen yerelde okutuldu:

> Küçük bir fark, ölçek değiştiğinde bambaşka bir dünyaya dönüşebilir.

Sıra: Antalia-2 Mini / tek ses; EMA Lightning / tek ses; Supertonic 3 M1–M5, sonra F1–F5. Model ve profil adları ekranda açık: bu video kör karşılaştırma değildir. Mevcut kör arayüz oturumu ve puanları değişmez. Model seçimi/silme yok.

Üretim: `npm run tts:reel`. Önce her modelin kendi venv’sinde seed42, CPU, doğal hız ile ağ erişimi engellenerek sentez, sonra iki geçişli mevcut loudnorm ile dinleme kopyası. Sesler sonradan hızlandırılmadı. `tts/outputs/mobile-reel/` master/metadata; `public/tts-voice-reel/` render varlıkları Git dışında. Render ayrı `src/voice-comparison.tsx` entry’sinden yapılır; ana Remotion composition kayıtlarına ve mevcut görsellere dokunulmadı.

Teslim `renders/tts-12-profiles.mp4`: 1080×1920, 30 FPS, 2086 kare, 69,533 saniye, H.264 + AAC192k, 2,70 MiB. Her ses öncesi0,2 sn, sonrası en az0,8 sn boşluk vardır. Son45 kare mevcut, değiştirilmemiş kanonik outrodur. Bu dinleme derlemesi yayın bölümü değildir; 40–45 sn bölüm sınırının dışında bir teknik karşılaştırmadır.

`python3 tts/qa_reel.py`: gerçek MP4 kare/süre/codec boyutu ve ses kontrolü. AAC’den decode edilen12 segmentin kaynak sesle korelasyonu >0,9998; ölçülen başlangıç örneği farkı en fazla16/48000 saniye (0,334 ms). Milisaniye tabanlı FFmpeg gecikme yuvarlaması doğrulamada hesaba katılır; kelime senkronu iddiası yok. Encode edilmiş mono ses peak0,8081’in altında; clipping yok. `tts/comparison/reel-qa.json` gerçek ölçümleri içerir.

Gerçek MP4’ten 1/2/3/7/8/12. profillerin kareleri çıkarıldı ve tek kontakt sayfasında görsel incelendi: metin, Türkçe karakterler, profil sırası, dalga biçimi ve güvenli yerleşim okunur. İnceleme dosyaları `renders/voice-comparison-review/` altında. Sesleri kulakla puanlamadım; kullanıcının dinlemesi içindir. TypeScript/lint/mevcut4 test/marka17 dosya kontrolü, TTS4 backend testi ve mevcut72 WAV QA geçti.

Mobil indirme için yalnız bu küçük inceleme MP4’ü kullanıcının yetkilendirdiği özel GitHub reposuna eklendi; büyük WAV’lar, ağırlıklar ve ortamlar eklenmedi.
