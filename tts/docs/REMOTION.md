# Bölüm sesini Remotion’a bağlamak

Kalıcı anlatıcı **Supertonic 3 / M1 erkek**, seçili doğal hızdır. `tts/config/narrator.json` tek ayar kaynağıdır. StyleProof/Yelda sesleri ve eski karşılaştırma çıktıları tarihsel varlık olarak korunur; Antalia/EMA yeniden kurulmaz.

Yeni bölümlerin güncel akışı [üretim rehberinde](../../docs/PRODUCTION_GUIDE.md):

```sh
npm run episode:prepare -- --id <id>
npm run episode:review -- --id <id>
npm run episode:render -- --id <id>
npm run episode:qa -- --id <id>
```

`src/episodes/<id>/production.json` içindeki kesin konuşma metniyle M1 sesi önce üretilir. Native master `tts/outputs/episodes/<id>/`, normalize WAV ve kelime/altyazı varlıkları `public/episodes/<id>/` altındadır. Ayrı yerel hizalama ortamı gerçek WAV'ı analiz eder. TTS ve hizalama render sırasında çalışmaz. Her ikisi de ilk model indirmesinden sonra OS ağ yasağı altında çevrimdışı çalışır.

Yerel incelemede zamanları ms veya ±1 kare düzelt. Sesi dinleyip kontrol ettikten sonra açık insan onayı ver. Kaydetmek onay değildir. SRT ve gömülü altyazı aynı kelime export'undan gelir. İnceleme öncesi render/QA için `--draft` kullan; yayın komutları metin/ses/ayar/model/hash ve insan inceleme kapısını zorunlu tutar.

Toplam video **40–45 saniye**, son **45 kare** ortak outro. Konuşma için 38,5 saniyelik alt sınır yoktur. Son kelimeden sonraki WAV sessizliği sonuç tutuşuna sayılır; sessizlik iki kere eklenmez. M1 otomatik hızlanmaz. Uzunsa anlatımı sadeleştir.

`loadNarration` yalnız build-time Node kodunda kullanılır; tarayıcıdaki TSX içine import edilmez. Varsayılanı yayındır; `loadNarration(id,{publication:false})` taslak yükler. Özgün TSX sahneleri `EpisodeComposition` kullanır ve registry'ye kaydedilir. Yayın yolunda elle hazırlanmış captions JSON tek başına onay sayılmaz.

## Tarihsel ham ses aracı

`npm run tts:episode -- --id <yeni-id> --text-file <metin.txt>` eski ham ses hazırlama komutudur. Mevcut klasörü ezmez, elle cue ithalini destekler; yeni forced-alignment yayın manifesti üretmez. Eski `--allow-extended-duration` bayrağı yalnız komut uyumluluğu için kabul edilir ve artık süre kuralını kaldırmaz. Yeni üretimde üstteki `episode:prepare` akışını kullan.

Geçmişte Git dışı `tts-integration-check` altında 43,315 saniyelik Antalia ham ses denemesi yapıldı. Bu tarihsel test yeni M1 entegrasyon testi değildir ve bu görevde yeniden üretilmedi. Güncel 40 saniyelik gerçek M1 MP4: `renders/episodes/production-check/draft.mp4`; [ölçüm ve inceleme kaydı](../../docs/PRODUCTION_QA.md).
