# Tasarım sistemi — 0.1-candidate

Modern bilim belgeseli ve editoryal bilgi görselleştirmesi. Nesne ve ilişki ana odak; sayı yardımcı kanıt. Ana zemin düz ve sabit. Her anda bir ana odak, en fazla iki yardımcı bilgi. Marka ancak açık kullanıcı talebiyle değişir.

Tek kaynak: `src/brand/tokens.ts`.

| Token | Renk | Kullanım |
|---|---|---|
| background | #111615 | Sabit ana zemin |
| foreground | #F2F0E9 | Kritik metin ve temel nesne |
| accent | #F07857 | Az miktarda odak ve işaret |
| secondaryAccent | #9DBFCA | Karşılaştırılan ikinci unsur |
| mutedText | #909B97 | Yardımcı ama okunabilir etiket |
| guideLine | #35413E | Düşük kontrastlı geometrik yardımcı çizgi |

Tanınırlık gerektiren gerçek nesnelerin doğal renkleri kullanılabilir; palet değiştirilmez. Neon, glow, cam kart, dekoratif gradyan, lens parlaması, parçacık yağmuru, emoji ve uyumsuz stok ikonlar kullanılmaz. Dashboard veya slayt kartı düzeni kurulmaz.

IBM Plex Sans 400/500/600: başlık ve anlatım. IBM Plex Mono 400/500: sayı ve ölçü. Resmî IBM paketlerinin tam WOFF2 dosyaları yerelde; `loadFont` render'ı yükleme bitene kadar bekletir. Türkçe glyph kapsamı ayrıca kontrol edilir; sessiz font değiştirme yok.

Başlangıç ölçeği: sayı 200 px (160–240), başlık 88 px (80–104), altyazı 46 px (44–52), ölçü 36 px (34–40). Küçük marka imzası 26 px ve style-board teknik açıklamaları özel kullanım istisnalarıdır. Başlık en fazla iki satır. Uzun metinde ifadeyi kısalt veya yerleşimi değiştir. Sayı biçimi `tr-TR`: 1.000.000 / 11,6.

1080×1920 güvenli başlangıç payları: sol72 / sağ144 / üst180 / alt300. Bunlar platform standardı değildir. Önemli metin alanı x72–936 / y180–1620. `StyleProofDebug` görünümü üretim MP4'üne dahil olmaz. Kamera geometriden sorumlu; metin ekran koordinatlarında kalır.

İşaret: 24/40/64 uzunluk, 10 aralık, 3 kalınlık, 6×6 mercan nokta. SVG `BrandMark` geometri tokenlarından orantılı üretilir. Küçük imza konumu x72/y184, genişliği64. Dünya/atom/galaksi/ampul/sonsuzluk simgesi yok.

StyleProof sayım geometrisi adedi anlatır; uzunluk/alan/hacim ölçüsü iddiası taşımaz. Bir kare bir birimdir. İlk on kare mercan, aynı yüzlük bloğun kalan doksanı buz mavisi; sonraki dokuz blok ön plan renginde. Kareler aynı anda aynı kamera ölçeğindedir.
