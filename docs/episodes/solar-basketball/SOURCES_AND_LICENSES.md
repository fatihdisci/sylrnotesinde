# Ölçek, kaynak ve haklar

Araştırma: 10 Ekim 2026. Bütün varlıklar renderdan önce yerel hazırlandı.

Tek ölçek: `modelMetres = realKilometres × 0.24 / 1_391_400`.

| Nicelik | NASA girdisi, km | Model değeri | Ekran / konuşma |
|---|---:|---:|---|
| Güneş çapı | 1.391.400 | 0,24 m | 24 cm |
| Dünya çapı | 12.756 | 2,20026 mm | 2,2 mm / iki milimetreyi biraz geçer |
| Güneş–Dünya | 149.600.000 | 25,80423 m | 25,8 m / yaklaşık 26 metre |
| Ay çapı | 3.474,8 | 0,59936 mm | 0,6 mm / yarım milimetre civarında |
| Dünya–Ay | 384.400 | 6,63044 cm | 6,6 cm / altı ila yedi santimetre |
| Jüpiter çapı | 142.984 | 2,46630 cm | 2,5 cm |
| Güneş–Jüpiter | 778.500.000 | 134,28202 m | 134,3 m / yaklaşık 135 metre |
| Güneş–Neptün | 4.515.000.000 | 778,78396 m | 778,8 m / yaklaşık 780 metre |

Hesaplanabilir kaynak: `src/episodes/solar-basketball/model.ts`. Ortalama mesafeler merkezden merkeze; NASA tablosundaki gezegen çapları ve Ay ortalama çapı kullanılır. Model yalnız anlatımdaki örnekleri içerir; gerçek yörünge yerleşimi göstermez. Ekran yuvarlamaları küre geometri/konumuna uygulanmaz.

NASA birincil tabloları: [Sun Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html), [Planetary Fact Sheet – Metric](https://nssdc.gsfc.nasa.gov/planetary/factsheet/), [Moon Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html). Güneş ortalama yarıçapı 695.700 km; Ay ortalama yarıçapı 1.737,4 km ikiyle çarpıldı. Basketbolun 24 cm çapı kullanıcı tarafından verilen model varsayımıdır.

Gezegen/Güneş/Ay haritaları: **Solar System Scope / INOVE**, [resmî texture sayfası](https://www.solarsystemscope.com/textures/), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Ticari kullanıma izin verir; atıf, lisans bağlantısı ve değişiklik belirtimi gerekir. Bu bölümde orijinal 2K haritalar küreye UV ile sarıldı; ışık, dönüş ve kamera kodda değişir. Haritalar NASA kaynaklarından türetilmiş, sanatsal olarak düzenlenmiş yüzeylerdir; yeni bilimsel görüntü sayılmaz. Dosya URL/SHA256/atıf listesi `public/episodes/solar-basketball/asset-manifest.json`. Yayımlanırken açıklamaya şu atıf eklenmeli:

> Planetary textures: Solar System Scope / INOVE, solarsystemscope.com/textures, CC BY 4.0. Rendered on 3D spheres with lighting and camera adjustments.

Basketbol derisi/bump, dikiş geometrisi, bina/sokak modelleri, kameralar ve müzik/efekt sentezi bu proje için özgün üretildi. Ödünç müzik, sample veya marka logosu kullanılmadı. IBM Plex lisans kayıtları mevcut font belgelerindedir.

Antalia-2 Mini: [resmî model kartı](https://huggingface.co/cloud0day3/antalia-mini), Apache-2.0 kod/normalizer/ağırlık; ticari senteze izin verir. `antalia-mini==1.0.0`, model revision `1e8166a7436f3e11f7f03b339258ec30f366db60`, Python 3.12.12, CPU, 48 kHz, tek sentetik erkek ses. Lisans/NOTICE `tts/licenses/antalia-mini/` içinde korunur. Seçili Supertonic/M1 ayarına dokunulmadı. Altyazı hizalayıcı `mpoyraz/wav2vec2-xls-r-300m-cv7-turkish`, sabit revision `708639f50559d7970f462e13ec64d3f059ca89f6`, CC BY 4.0; mevcut yerel CTC Viterbi altyapısı kullanıldı.
