# Bölüm sesini Remotion’a bağlamak

Görsel proje, StyleProof ve outro değiştirilmedi. Mevcut `assets:voice` Yelda denemesi geçmiş görsel testin kaynağı olarak korundu. Kullanıcı yeni bölümler için **Supertonic 3 / M1** seçti. `tts/config/narrator.json` tek ayar kaynağıdır; model/profil belirtmeden CLI bu seçimi kullanır. Doğal hız1 korunur; her bölümün gerçek ses süresi ayrıca doğrulanır. Seçili anlatıcı, her üretilen dosyanın altyazı/ses incelemesinin tamamlandığı anlamına gelmez.

Ortak CLI modellerin kendi venv’lerine subprocess ile gider. Animasyon kodu PyTorch/ONNX/TTS import etmez. `render.ts` ses üretmez, hazırlanmış WAV okur. Sahne süreleri gerçek ses süresinden hesaplanır; son 45 kare kanonik outroya ayrılır.

```sh
# Merkezi seçimden Supertonic 3 / M1 kullanılır.
npm run tts:episode -- --id yeni-bolum --text-file anlatim.txt
```

Bu komut native master ve metadata’yı `tts/outputs/episodes/yeni-bolum/` altında tutar, eşitlenmiş WAV’ı `public/episodes/yeni-bolum/narration.wav` olarak hazırlar. `narration-manifest.json` alanları mevcut türlendirilmiş `Episode` yapısının `narration`, `audio`, `subtitlePath`, `captions` alanlarıyla uyumludur. Önerilen kare sayısı gerçek WAV +45’tir; 40–45 saniyelik toplam bölüm kuralını denetler. Daha kısa/uzun taslakta `--allow-extended-duration` yalnız üretim/inceleme için açık istisnadır; `loadNarration` yine geçersiz bölüm süresini kabul etmez.

Mevcut bölüm varlık klasörünü ezmez. Düzeltme gerektiğinde yeni revision ID kullan. Bir giriş metnini değiştirmek eski WAV’ın kendiliğinden güncellendiği anlamına gelmez; yeniden üretim ve süre kontrolü yapılır.

Altyazı ilk adımda boş ve `captionReviewRequired=true` olur. EMA model zamanları metadata içinde tutulur, kusursuz hizalanmış sayılmaz. Diğer adaylar zaman etiketi sağlamaz. Uydurma sözcük zamanları üretilmez. Dinleyerek kısa anlam öbekleri için şu JSON hazırlanır:

```json
[
  {"from": 0, "to": 76, "lines": ["İlk anlamlı anlatım öbeği."]},
  {"from": 79, "to": 154, "lines": ["İkinci öbek en fazla", "iki satırdır."]}
]
```

Örnekteki kareler yalnız dosya biçimini gösterir; gerçek sese ait doğrulanmış zamanlar değildir. `--captions kontrol-edilmis.json` ile **yeni revision ID’ye** export edilir. Komut aralıkları, çakışmayı, iki satır sınırını ve ses süresini denetler; bu yapısal kontrol insanın ses/görsel incelemesinin yerine geçmez.

Yeni bölümün build-time kodunda:

```ts
import {loadNarration} from '../../../scripts/load-narration';
// Build-time Node scriptinde çalıştır, sonucu bölüm veri dosyasına yaz.
const prepared = loadNarration('yeni-bolum');
// Episode verisine narration/audio/subtitlePath/captions alanlarını aktar.
// Özgün TSX sahnelerini gerçek ses işaretlerine göre tasarla.
```

`loadNarration` Node dosya okuması kullandığı için tarayıcıdaki TSX bileşenine import edilmez; bölüm hazırlama/build scriptinde çalışır. Gözden geçirilmemiş altyazıyı, eksik WAV’ı, geçersiz marka/FPS’yi veya outroya taşan sesi reddeder. Son Episode için mevcut `validateEpisode` ve görsel/render QA da uygulanır. Ses sağlayıcısı/voice ID/speed/seed ve kaynak model revision’ları metadata’da kalır; API anahtarı yok.

Gerçek entegrasyon denemesi bu Mac’te `public/episodes/tts-integration-check/` altında 43,315 saniyelik Antalia sesi ve 1345 kare (44,833 sn, outro dahil) manifest üretti. Taslak altyazı kontrolü bekliyor; yayımlanacak bölüm veya yeni görsel composition kaydedilmedi. Bu deneme Git dışıdır. Üretim aracı test edildi; tam anlatımlı yeni bir Remotion bölüm render’ı bu görevde görselleri değiştirmemek için yapılmadı.
