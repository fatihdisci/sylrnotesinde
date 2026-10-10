# Güneş Bir Basketbol Topu Olsaydı?

Özgün fikir: **Avuç içinden bir mahalleye.** Kamera önce topun deri dokusunun içindedir. Geri çekilme tanıdık nesneyi açığa çıkarır; dikişli deri aynı çapı koruyarak Güneş yüzeyine dönüşür. Kesilen yakın planlar aynı fiziksel dünyadaki Dünya, Ay, Jüpiter ve Neptün modellerine gider. Milimetrelik Dünya’dan geri çekilince gece sokağı belirir. Son yolculuk 779 metre boyunca ilerler, sonra bütün mahalleye yükselir.

Yakın planlarda küre çapları değiştirilmez. Kamera mesafesi değişir. Şehir, özgün kodla üretilmiş temsili bir model çevresidir; gerçek bir adres veya uydu görüntüsü değildir. Cisimler ortalama merkez uzaklıklarını karşılaştırmak için aynı doğruya yerleştirilir; bu, gezegenlerin aynı anda gökyüzündeki konumları veya yörüngeleri değildir. Geniş planda konum işaretleri küre boyutlarını temsil etmez; bu varsayımlar üretim belgelerinde saklanır. Kullanıcı tercihiyle altyazı üstündeki küçük açıklamaların tamamı kaldırılmıştır; bu katman gelecek videolara da eklenmez.

Bu bölüme özgü gece laciverti, doğal gezegen renkleri, deri yüzeyi, sıcak pencere ışıkları ve metre cinsinden 3D mimari kullanıldı. IBM Plex, mercan/buz mavisi vurgu, köşe imzası ve kanonik outro korunur. `src/brand` ve korunan `EpisodeComposition` değişmez. Atmosferik derinlik yalnız kamera uzaklığına bağlı sisle hesaplanır. Sabit yıldızlar bir yağmur/rasgele animasyon değildir. Bütün hareket `useCurrentFrame` ve ölçülmüş kelime çapalarından gelir.

- 0–10,74 s: doku → basketbol → aynı çaplı Güneş.
- 10,74–17,29 s: Dünya makrosu, ince iğne desteği; 2,2 mm çap.
- 17,29–29,91 s: milimetreden 25,8 m sokağa; ileri dolly ve yeniden yaklaşma.
- 29,91–36,87 s: Dünya–Ay ortak ölçeği, 6,6 cm aralık ve Ay ayrıntısı.
- 36,87–45,91 s: Jüpiter yüzeyi → 134,3 m yolculuk.
- 45,91–53,02 s: Neptün yüzeyi → yüzlerce metre boyunca yükselen uçuş.
- 53,02–64,47 s: yaklaşık 800 m rotayı kapsayan mahalle; son cümle ve kısa sonuç tutuşu.
- 64,47–65,97 s: değişmemiş 45 kare outro.

Kesin kareler `src/episodes/solar-basketball/storyboard.json` sözcük çapalarından çözülür. Çözülen tablo `public/episodes/solar-basketball/storyboard.md`; kamera ve ses efektleri bu olayları kullanır. Yukarıdaki yuvarlak saniyeler bağımsız altyazı kaynağı değildir.

Ses: tek erkek Antalia-2 Mini, doğal göreli hız 1, seed 42, Apple Silicon CPU. Eski M1 seçimi merkezî konfigürasyonda korunur. Bu bölüm açık kullanıcı isteğiyle Antalia kullanır. Kullanıcı düzeltmesiyle hışırtılı whoosh ve noise katmanları kaldırıldı. Yerlerinde yumuşak sinüs temelli blink/bip, kısa uyumlu nota dizileri ve 84 BPM özgün ritmik bir arka plan (yumuşak bas, kısa melodik notalar ve tonal vurmalılar) bulunur. Olayların başlangıç kareleri aynı storyboard çapalarındadır; yumuşak atak ve sönümler keskin tıklamaları önler. Sesler uzayda fiziksel ses yayılması iddiası taşımaz. Gerçek anlatım RMS’i miksin yan zincirini kontrol eder. İnsan dinleme onayı verilmiş sayılmaz.

Güncel ses dengesi kullanıcı isteğiyle `src/episodes/solar-basketball/audio-mix.json` içinde tutulur: anlatıcı 0,40, efekt 1,00, ambient 0,17. Ses hazırlama scripti, render bileşeni ve MP4 QA aynı kaydedilmiş gain’leri kullanır.

Bu ses karakteri ve denge, kullanıcı isteğiyle [kalıcı üretim talimatlarına](../../AUDIO_STYLE.md) kaydedildi.
