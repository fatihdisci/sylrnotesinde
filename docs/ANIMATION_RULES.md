# Animasyon kuralları

Tek saat `useCurrentFrame()`. Süre FPS üzerinden kareye çevrilir. CSS keyframe/transition, setTimeout, Date.now, performance.now veya kontrolsüz Math.random ile hareket üretme. Gerekli rastgelelikte sabit seed kullan.

Ortak hareket: cubic-bezier(0.22, 1, 0.36, 1). `src/brand/motion.ts`: yazı/etiket12 kare, ölçüm20 kare, kamera54 kare. Makul aralıklar sırasıyla8–14 /15–24 /30–60 kare. Varsayılan zıplama veya overshoot yok. Sahnenin anlamı gerektiriyorsa tempo değişebilir.

Yaklaşma ayrıntıyı, uzaklaşma ölçek farkını açığa çıkarır. Önceki nesne veya çizgi sonraki sahneye bağlanır. Her sahne için rastgele geçiş seçme. Ekran etiketleri kamera dönüşümünden ayrı tutulur.

StyleProof'ta ilk24 karede tek şerit on birime ayrılır. f90–144 kamera100 birime, f210–270 kamera1.000 birime açılır. Sayılan kareler görünür kameranın içinde kalır; ara karelerde sayaç tam çizilen adetle eşleşir. Tüm örnekler en fazla1.000 SVG rect ile çalışır. Devasa adetlerde toplu SVG path, Canvas veya açıkça etiketli örnekleme kullan; milyonlarca DOM elemanı üretme.

Uzunluk/alan/hacim doğruluğunu ayrı kontrol et. Alan oranı için kenar oranı karekök, hacim oranı için küpkök gerektirir. Şematik veya logaritmik gösterimi etiketle. Nokta/grup birçok nesneyi temsil ederse karşılığını yaz.

Outro tek sahipli: `src/brand/Outro.tsx`, prop almaz. 45 kare: ilk12 çizgiler, 12–24 mercan işaret, ilk20 içinde isim; kalan sürede tut. İlk karede çok kısa çizgi parçası vardır, boş zemin karesi yok. İki hafif tık f2/f10, yumuşak tok ses f22'de başlar. WAV 1,5 s; kuyruk1,16 s'den önce söner. Üretim scripti deterministiktir; render ses üretmez.

`LayoutProbe` yalnız debug içindir; font hazır olunca DOM ölçer. Zaman tabanlı hareket oluşturmaz ve finalde çalışmaz.
