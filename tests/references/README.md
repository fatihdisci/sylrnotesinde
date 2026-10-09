# İlk aday referansları

9 Ekim 2026'da gerçek MP4 kareleri incelendikten ve yerleşim düzeltildikten sonra ilk kez kaydedildi. Sürüm **0.1-candidate**; bu kayıt kullanıcı onayı değildir.

- opening.png: StyleProof f30
- hundred.png: StyleProof f180
- result.png: StyleProof f360
- outro.png: Outro f24
- board.png: StyleBoard f0

PNG'ler MP4 sıkıştırmasından bağımsız Remotion still renderlarıdır; gerçek MP4 inceleme kareleri `renders/qa/` içindedir. Referanslar burada ilk aday tasarımın regresyon kontrolü içindir.

`brand-manifest.json` marka kaynaklarını, yerel fontları, sabit WAV'ı, ses üretim scriptini ve ortak bölüm zarfını SHA-256 ile kaydeder. Referans/toleransları kontrol geçirmek için yenileme. Marka değişikliği açık kullanıcı talebi gerektirir; değişikliği raporla, önceki referansları koru.
