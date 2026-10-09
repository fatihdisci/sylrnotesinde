# Kalıcı anlatıcı — kullanıcı seçimi

Kullanıcı “M1 erkek sesini seçiyorum” dedi. Aktif anlatıcı **Supertonic 3 / M1**; kalite sıralaması otomatik yapılmadı. Tek ayar kaynağı `tts/config/narrator.json`: Türkçe, CPU, seed42, göreli hız1 (model içi1,05). Seçilmiş model revision’ı, ONNX Runtime1.23.1, kilit ve lisans değişmedi.

## İki cihazda kullanım

```sh
# MacBook’ta repo güncellemesinden / ilk klondan sonra:
npm ci
npm run tts:setup
npm run tts:generate -- --text 'Küçük bir fark, ölçek değiştiğinde bambaşka bir dünyaya dönüşebilir.' --output tts/outputs/manual/m1.wav --os-offline
# Gerçek bölüm metni hazır olduğunda:
npm run tts:episode -- --id yeni-bolum --text-file anlatim.txt
```

Varsayılan kurulum yalnız seçili modelin ortamını ve ağırlıklarını kurar. MacBook’ta bu oturumdan fiilen test yapılmadı. Ağırlıklar/venv/çıktı WAV’ları Git dışıdır; her cihazda bir kez indirilir. Render TTS çalıştırmaz. M1’in önceki93 kelimelik D metni doğal hızda48,10 sn sürdü; 40–45 sn bölüm hedefi için metin gerçek sese göre kısaltılır veya hız ayrıca dinlenerek ayarlanır. Varsayılan hız kendiliğinden yükseltilmedi.

`src/episodes/narrator.config.ts` yalnız mevcut StyleProof/Yelda testini yeniden üretmek içindir. Mevcut video, görsel kimlik ve outro değişmedi. Yeni bölüm sesinin altyazıları ve son sözcükleri ayrıca kontrol edilir; seçilen ses, otomatik sözcük senkronu veya tamamlanmış bölüm QA’sı anlamına gelmez.

## Güvenli temizlik

Yalnız bu proje altındaki Antalia/EMA venv, ağırlık ve kaynak klonları kaldırıldı: altı dizin,994.750.331 dosya baytı (yaklaşık949 MiB; diskte kazanılan blok miktarı ayrıca ölçülmedi). Her hedefin proje içinde, sembolik bağlantı olmayan ve Git’te izlenmeyen dizin olduğu silmeden önce doğrulandı. Tam kayıt `tts/config/selection-record.json`.

Supertonic’in ortamı, ağırlıkları ve diğer küçük profil dosyaları korunur. Sistem/ortak Python’a ve başka projelere dokunulmadı. Kurulum bootstrap’ı, proje Python runtimeları ve ortak kurulum önbelleği tutuldu. Karşılaştırma WAV’ları, MP4, kullanıcı puanları, ölçümler, model kilitleri ve lisanslar arşiv olarak korunur. Karşılaştırma arşivi için eski modelleri açıkça geri kurmak mümkündür: `npm run tts:setup -- --all`. Varsayılan komut onları geri indirmez.

Supertonic kodu MIT, ağırlıkları OpenRAIL-M; önceki lisans incelemesi ve tam metin `INSTALLATION.md` ile `licenses/supertonic-3/` altında korunur. Yapay zekâ seslendirmesi açıklama şartı yayın sırasında uygulanır.

## Seçim sonrası doğrulama

- Temizlik sonrasında `npm run tts:setup`: yalnız Supertonic ortamı ve19 varlık doğrulandı; Antalia/EMA geri kurulmadı.
- Model/ses belirtmeyen gerçek CLI sentezi OS ağ yasağı altında M1 üretti: 5.046 sn WAV / 1.016 sn sentez / 523.7 MiB tepe RSS. Decode edilmiş PCM, kullanıcının dinlediği mobil karşılaştırmadaki M1 ile birebir aynı.
- Eşitlenmiş48 kHz PCM24 dinleme kopyası: -20.17 LUFS, -2.01 dBTP; sonlu, dolu ve clipping yok. Kayıt `config/selected-narrator-qa.json`.
- `npm run tts:offline`: OS ağ reddi socket probu geçti; bağımsız M1 A tekrarı eski corpus ile aynı PCM, ağ girişimi yok. Kayıt `config/active-offline-test.json`; önceki üç model raporu korundu.
- `npm run tts:qa`: korunmuş72 dinleme WAV’ı, sıfır hata. QA araçları artık kaldırılmış Antalia ortamına bağımlı değil.
- `npm run tts:test`:7 test geçti. `npm run check`: TypeScript, ESLint,4 proje testi ve17 korumalı marka dosyası geçti.
- MacBook’ta çalıştırma, yeni bölüm render’ı, sözcük hizası ve kulakla öznel kalite değerlendirmesi bu seçim işleminde yapılmadı. Kullanıcının ses seçimi kalite test puanına dönüştürülmedi.
