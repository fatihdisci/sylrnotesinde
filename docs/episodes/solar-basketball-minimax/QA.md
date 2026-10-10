# MiniMax Güneş filmi — gerçek çıktı QA

İnsan dinleme onayı verilmemiş ayrı MiniMax sürümü. Mevcut filmler ve TTS kurulumları korunur.

- Gerçek MP4:1080×1920,30 FPS,2361 kare /78,7 saniye. Outro2316. karede /77,2 saniyede başlar,45 kare sürer. Son ölçülen kelime75,970 saniyede biter; sonucu tutmak için1,2 saniye ayrılır. Kaynak ses hızlandırılmadı/kesilmedi.
-143 kelime ve33 cue gerçek WAV'dan yerel Türkçe CTC Viterbi ile hizalandı. Sayısal ekran metni ve konuşma öbekleri açık word-ID eşlemesiyle bağlıdır. SRT ve gömülü cue verisi aynı kaynaktan ve aynı30 FPS yuvarlama kuralından çıkar; eşitlik kontrolü geçti.
- MP4 AAC baş/orta/son kaynak ses karşılaştırmaları:0 ms gecikme,0 ms ölçülen drift; korelasyonlar>.9998.22 storyboard ses/görüntü olayının miks karşılaştırması geçti. Outro0 ms gecikme ve.99999 korelasyon. Bunlar kodlama/zaman çizelgesi kontrolüdür, her kelimenin fonetik sınırını garanti etmez.
- Nihai MP4:−27,50 LUFS /−12,17 dBTP; clipping yok. Kullanıcının kalıcı düşük anlatıcı miks tercihi korundu. Genel−25..−17 LUFS kapısı BAŞARISIZ; eşik değiştirilmedi. Kalan medya kontrollerini ölçen geçici diagnostic çalışması yalnız LUFS aralığı şartını atladı; rapor technicalChecksPassed=false / loudnessPolicyPassed=false tutar. Geçici script silindi, genel QA kodu değiştirilmedi.
- Siyah aralık ve boş içerik karesi yok.142 küçük geometri karesi ve dört büyük kare farkı inceleme adayı; bunlar ölçek gereği küçük cisim/gezegen yakın plan geçişleridir, dedektör öznel titreme kararı vermez. Dokuz gerçek MP4 örnek karesi görsel olarak incelendi; Türkçe karakterler, en fazla iki satır altyazı, açılış/Dünya/sokak/Ay/Jüpiter/Neptün/sonuç/outro görüldü.22. saniyede boyuttan uzaklığa kamera çekilmesi nedeniyle nesne küçük ve plan karanlıktır; aynı önceki görsel tasarım korundu. Tüm hareketli videonun insan tarafından izlenmesi yapılmadı.
- Otomatik tanı15 kelimeyi işaretledi; ayrıca “küçültseydik,” ile “Dünya” arasında2,890–3,260 saniyelik aralıkta enerji bulundu. Waveform tanısında enerji yaklaşık2,99 saniyeye kadar sürüyor; bu bir önceki sözcüğün kuyruğu olabilir. İki kelime zaten aynı altyazı öbeği içindedir. Kulakla doğrulanmadan sınır veya gap onayı yazılmadı. Yerel editörde özellikle bu aralık ve15 kelime dinlenmeli. PublicationReady=false korunur.
- TypeScript/lint/21 TS testi/17 korunan marka dosyası kontrolü geçti. Üretim testleri16 geçti/1 tarihsel harici ses fixture'ı skip; hizalama testleri5 geçti. Yeni TTS, API çağrısı, model/venv değişikliği yok.

Çıktı: `deliveries/solar-basketball-minimax/gunes-basketbol-minimax.mp4`. SRT aynı klasörde. Ayrıntılı `technical-qa.json` içinde ölçümler ve şüpheli kelime ID'leri vardır. Kelime JSON'u `public/episodes/solar-basketball-minimax/word-timings.json`.

İnceleme: `npm run episode:review -- --id solar-basketball-minimax`. Yapılmamış insan dinlemesi veya onayı başarılı sayılmadı.

Gerçek Chromium yerleşim kontrolü138 karede geçti: taşma/çakışma yok, tüm IBM Plex fontları yüklü. Altyazısız kontrol kareleri aynı zamanlarda ayrıca render edildi; yerel `renders/episodes/solar-basketball-minimax/review/` içinde saklanır.

Kaynak MP3 ve yerel arşiv byte eşitliği, eski Güneş MP4 SHA256 ve yeni teslim MP4/render provenance SHA256 karşılaştırmaları geçti. Üç altyazısız kontrol görüntüsü ayrıca görsel olarak incelendi. Genel episode:qa son aşamada yalnız belgelenen LUFS aralığı koşulunda durdu; yerleşim ve kaynak bütünlüğü kontrolleri geçti.
