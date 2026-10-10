# Chatterbox V3 — gerçek çıktı kontrolü

Durum: kullanıcı dinleme adayı; yayın onayı yok. Aynı Güneş/basketbol filmi yeni sesle yeniden render edildi. Hiçbir otomatik doğal ses kalitesi iddiası yapılmaz.

- Native ses: 24 kHz, 72,16 saniye. CPU4 thread: 239,70 saniye duvar süresi, 931,98 CPU saniyesi, 5,31 GiB azami RSS. OS ağ engeli altında gerçek üretim, sıfır ağ girişimi.
- Video: 1080×1920, 30 FPS, 2227 kare, 74,233 saniye. Outro 2182. kareden itibaren45 kare.
- Türkçe yerel wav2vec2 CTC hizalama:144 kelime,32 altyazı öbeği.15 şüpheli kelime inceleme bekliyor. Otomatik veriler onaylanmış sayılmadı.
- Nihai AAC sesinin baş/orta/son eşleşmesi:0 ms kayma,0 ms ölçülen drift; korelasyon>.9999.22 ses/görüntü olayının miks eşleşmesi geçti. Outro kayması−0,33 ms. Bunlar dosyaların zaman çizelgesini doğrular; her kelimenin fonetik doğruluğunu kanıtlamaz.
- WAV QA geçti:−20,01 LUFS,−2 dBTP. Nihai kullanıcı tercihli düşük miks:−27,65 LUFS /−12,16 dBTP. Genel−25..−17 LUFS koşulu BAŞARISIZ; eşik değiştirilmedi. Diagnostic rapor kalan kontrolleri ölçmek için yalnız bu koşulu atladı ve technicalChecksPassed=false bıraktı.
- Siyah aralık/boş içerik bulunmadı. Küçük ölçekte nesne gösteren bazı kareler geometri dedektörünce işaretlendi; bunlar tek başına bozuk kare kanıtı değildir.357,637,1048,1227,1409,1567,1943,2196. gerçek MP4 kareleri ve yedi10 saniyelik örnek görsel olarak incelendi.637. karede nesne bilinçli biçimde çok küçüktür; kullanıcı hareketli oynatımda okunabilirliği değerlendirmeli. Kesit adayları1227/1409/1567 yeni büyük gezegen/mesafe planlarına denk gelir. Tüm hareketin insan tarafından izlenmesi yapılmadı.
- IBM Plex fontları, marka ve eski video korundu.17 korunan marka dosyası kontrolü geçti; eski teslim MP4 SHA256 değişmedi. Supertonic47 dosyalık ortam/model/ayar hash kontrolü geçti.
- TypeScript, lint,21 TypeScript testi;9 TTS testi;5 hizalama testi geçti.17 üretim testinin16'sı geçti, tarihsel eksik harici ses fixture'ı nedeniyle1 mevcut skip. Yeni WAV QA1/1 geçti.

İnsan dinlemesi yapılmadı: telaffuz, son heceler, sesin hoşluğu ve15 işaretli kelime kullanıcı tarafından dinlenmeli. Altyazı editörü: `npm run episode:review -- --id solar-basketball-chatterbox-tr`. Yayın render'ı inceleme tamamlanmadan engellenir.

Teknik ayrıntı: `technical-qa.json`; örnek kareler `deliveries/solar-basketball-chatterbox-tr/`. Orijinal film, Antalia ve kalıcı Supertonic/M1 anlatıcı ayarı korunur. Chatterbox V3 bu bölümde mevcut sentetik M1 Türkçe örneğiyle koşullandırılmıştır; yeni insan ses kaydı veya model eğitimi kullanılmadı.

İlk yerleşim denetimi1943. karede Güneş/Jüpiter metin sınırlarının2,73 px çakıştığını buldu. Yalnız yeni bölüm wrapper’ında Jüpiter etiketini18 px yukarı ayıran statik SVG transform eklendi; eski sahne ve marka kaynaklarına dokunulmadı. Son MP4 bu düzeltmeyle yeniden üretildi.

Son yerleşim denetimi139 karede geçti:0 taşma,0 çakışma; beş IBM Plex fontu yüklü; altyazılar en fazla iki satır. Altyazılı gerçek MP4 örnekleri ve eş karelerin altyazısız kontrol çıktıları yerel `renders/episodes/solar-basketball-chatterbox-tr/review/` altında.
