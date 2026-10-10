# Kalıcı ses tasarımı tercihi

Kullanıcı tarafından art arda yapılan dinleme geri bildirimlerinin sonucu: konuşma aşırı baskın olmayacak; görselle senkron blink/bip efektleri belirgin duyulacak ve arka planda hoş, hafif ritmik müzik bulunacak.

- Referans: `solar-basketball` güncel miks. Anlatıcı 0,50; efekt 1,00; müzik 0,17. Bölüm ayarı `src/episodes/solar-basketball/audio-mix.json` içindedir.
- Yeniden kullanılabilir ses bankası: `production/solar_sound.py` içindeki `effect()` ve `rhythmic_bed()`. Mevcut temiz enstrüman karakterini koru; efekt başlangıçlarını her bölümün gerçek anlatım/storyboard olaylarına bağla. Kaynak kod ve beste yereldir.
- Efektler yumuşak atak/sönümlü, temiz tonal blink/bip ve kısa uyumlu nota dizileri olsun. Hışırtı, noise tabakası ve gürültülü whoosh kullanma. Efektleri ancak işitilemeyecek kadar kısmak çözüm değildir.
- Arka plan yalnız sabit bir uğultu olmasın. Referans beste 84 BPM, 4/4; kısa melodik notalar, yumuşak bas ve tonal vurmalılardan oluşur. Yeni bölümün ritmine göre özgün bir düzenleme yapılabilir; aynı melodiyi zorunlu kılma.
- Konuşma anlaşılır kalsın, fakat diğer katmanları örtmesin. Konuşma sırasında kontrollü ducking uygula; müzik ve efektler hâlâ duyulur olsun.
- Bu gain sayıları mevcut kaynak WAV ve stem seviyeleri içindir. Yeni kaynakların yüksekliği farklıysa aynı algısal dengeyi hedefle; sayıları körlemesine kopyalama. Referans anlatıcı kaynak WAV’ı yaklaşık −20 LUFS düzeyindedir.
- Anlatıcı hızı veya ses profili bu miks tercihi nedeniyle değiştirilmez. Kanonik outro sesine dokunma; müzik ve efekt kuyrukları outroyu taşmasın.
- Miks ayarlarını bölümle birlikte kaydet. Nihai MP4 sesini decode ederek clipping, kayma ve miks bütünlüğünü kontrol et. Yapılmamış işitsel incelemeyi onaylanmış sayma.

Bu tercih yeni videolarda varsayılandır; kullanıcı açıkça farklı bir yön istemedikçe tekrar sormadan uygula. Altyazıların üstüne küçük açıklama katmanı eklememe kuralı da devam eder.
