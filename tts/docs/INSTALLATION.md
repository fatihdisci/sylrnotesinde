# Yerel TTS kurulumu · 2026-10-09

Bu altyapı Apple Silicon macOS üzerinde doğrulandı. Sistem Python’u ve başka projelerin ortamları değiştirilmez. Kullanıcı **Supertonic 3 / M1** seçti (`config/narrator.json`). Antalia/EMA ortamları, ağırlıkları ve kaynak klonları bu projeden kaldırıldı. Aşağıdaki üç aday tablosu ilk karşılaştırmanın teknik kaydıdır; güncel kullanım ve temizlik kaydı: [SELECTION.md](SELECTION.md). Ücretli API, bulut sentezi veya uzaktan sunucu yok.

## Doğrulanan adaylar

| Aday | Resmî kaynak / sürüm | Python | CPU / Apple Silicon | Sesler | Yerel hız |
|---|---|---|---|---|---|
| Antalia-2 Mini | [cloud0day3/antalia-mini](https://huggingface.co/cloud0day3/antalia-mini), `antalia-mini==1.0.0` | >=3.10; burada 3.12.12 | PyTorch 2.10.0 arm64 CPU; MPS isteğe bağlı ve burada çalıştı | Tek sentetik erkek ses, `default` | 0,95 |
| EMA Lightning | [canberk7/ema-lightning](https://github.com/canberk7/ema-lightning), `ema-lightning==1.0.4` | Resmî rehber 3.11–3.13; burada 3.12.12 | PyTorch CPU; MPS burada gerçek sentezle denendi | Tek sabit ses, `default` | 1,00 |
| Supertonic 3 | [resmî arşiv kodu](https://github.com/supertone-oss-archive/supertonic), [orijinal ağırlık kaynağı](https://huggingface.co/Supertone/supertonic-3) | Resmî örnek 3.11; burada 3.11.15 | ONNX Runtime 1.23.1 arm64, CPUExecutionProvider; bu uygulamada MPS yok | M1–M5 erkek, F1–F5 kadın; Türkçe `tr` | 1,05 |

**Antalia-2 Mini gerçekten mevcut.** Üreticinin Hugging Face model kartı açıkça bu adı kullanıyor. PyPI 1.0.0 wheel SHA256’sı model deposundaki wheel ile eşleşiyor: `bd591ba87e2e53de62abc3b261476bbce8af5bbc7b60a451f46cc3b7e73aa8f2`. Kullanıcının verdiği `0daycloud/antalia` ve `cloud0day3/antalia-1` eski Antalia 1’e işaret ediyor. Eski kaynak incelendi; Mini doğrulandığı için Antalia 1 ağırlıkları kurulmadı ve başka isimle sunulmadı. İncelenen kaynak klonları bu Mac’te `tts/vendor/` altında korunuyor.

Supertonic kaynak README’sinin yönlendirdiği resmî arşiv ağırlıkları `supertone-oss-archive/supertonic-3` kullanıldı. PyPI’deki eski otomatik model indiren SDK yerine, sürümü sabitlenmiş resmî ONNX örneği çalıştırılıyor.

Tam model revision’ları, dosya boyutları ve LFS SHA256 değerleri `../config/models.json`; tüm yerel varlıkların SHA256 değerleri `../config/asset-checksums.json` içinde. Bağımlılıklar `../locks/*.txt` ile kilitli. Supertonic helper kaynak commit’i `1e9799e964ea4c0dad7cde993b65c3c813a7b373`; `adapters/supertonic_helper.py` bu commit’in `py/helper.py` dosyasının değiştirilmemiş kopyasıdır. MIT lisansı `licenses/supertonic-3/CODE-LICENSE` içinde.

## Kalıcı kullanım

```sh
npm run tts:setup  # yalnız Supertonic 3
npm run tts:generate -- --text 'Ölçek değişir.' --output tts/outputs/manual/ornek.wav --os-offline
npm run tts:episode -- --id yeni-bolum --text-file anlatim.txt
```

`--model` ve `--voice` verilmezse seçili Supertonic 3 / M1 kullanılır. Göreli hız1, CPU ve seed42 korunur. Eski Antalia/EMA örnek komutları ancak açık yeniden kurulumdan sonra kullanılabilir.

## Karşılaştırma arşivi — bu Mac’te

Proje kökünde:

```sh
npm run tts:compare
# http://127.0.0.1:3030
```

3030 zaten çalışıyorsa ikinci bir sunucu başlatma; açık arayüzü kullan. Farklı port: `npm run tts:compare -- --port 3032`. Sunucu yalnız loopback’e bağlanır, LAN’a açılmaz. Durdurma: terminalde Ctrl+C. Sonraki açılışta kayıtlar yüklenir.

```sh
npm run tts:generate -- --model antalia-mini --voice default --text 'Bir sıfır, ölçeği değiştirir.' --speed 1 --output tts/outputs/manual/deneme.wav --os-offline
npm run tts:generate -- --model ema-lightning --text-file tts/test-texts/long-narration.txt --output tts/outputs/manual/ema.wav --os-offline
npm run tts:generate -- --model supertonic-3 --voice F3 --text 'Ölçek değiştiğinde ilişki görünür olur.' --output tts/outputs/manual/f3.wav --os-offline
```

`--speed 1` modelin doğal varsayılanıdır; adapter gerçek parametreye çevirir. Ses sonradan hızlandırılmaz. Metin, model, ses, hız, çıkış yolu ortak arayüzdür. `--model` verilmezse merkezi aktif anlatıcı okunur; artık Supertonic 3 / M1 kullanır. `--device mps` yalnız iki PyTorch adayında denenebilir; varsayılan CPU.

## MacBook’a geçiş

Apple Silicon MacBook’ta Git, Python 3.8+ (yalnız bootstrap için), Node 22.22.3 ve ffmpeg gerekir. Remotion tarayıcısı ilk kullanımda yerel hazırlanır. ffmpeg yoksa kullanıcının tercih ettiği yerel paket yöneticisiyle kurulur; bu script sistem paketlerini değiştirmez.

```sh
git clone https://github.com/fatihdisci/sylrnotesinde.git
cd sylrnotesinde
npm ci
npm run tts:setup
npm run tts:generate -- --text 'Ölçek değişir.' --output tts/outputs/manual/ornek.wav --os-offline
npm run tts:offline
# Yeni bölüm için: npm run tts:episode -- --id yeni-bolum --text-file anlatim.txt
# Karşılaştırma arşivi gerekiyorsa açıkça:
# npm run tts:setup -- --all
# npm run tts:benchmark
# npm run tts:qa
# npm run tts:test
# npm run tts:compare
# Görsel proje için:
npm run browser:prepare
npm run preview
```

`tts:setup` proje içi bootstrap venv’de `uv==0.12.24` kullanır. Varsayılan olarak yalnız seçili modelin CPython 3.11.15 sürümünü; açık `--all` ile ayrıca 3.12.12’yi `tts/environments/python/` altına indirir, Python kısayollarını da yalnız `tts/environments/bin/` altına koyar. Model başına ayrı venv + kilit kullanır; sistem ortamına pip kurulumu yapmaz. Ağırlıklar sabit revision’dan indirilir, mevcut dosyalar doğrulanır. Yaklaşık 3 GB boş alan ayırmak yeterlidir; Python/venv/üretim miktarına göre ek pay bırak.

Kod, lisanslar, kilitler, metinler ve Mac mini ölçüm kayıtları Git’te. Ağırlıklar, ortamlar, büyük WAV’lar ve kullanıcı puanları Git’te değildir. MacBook’ta yeniden kurulum ve benchmark bu dosyaları yerelde oluşturur. Venv klasörünü iki cihaz arasında kopyalama. İlk indirme internet ister; sonraki sentez istemez. Aynı seed/sürüm bu Mac’te aynı PCM örneklerini verdi; farklı donanımda bit düzeyinde eşitlik garantisi verilmez.

Sonuçlarını taşımak için arayüzden JSON indir. Tamamlanmış JSON gerçek kimlikleri de içerir. Sürmekte olan kör oturumu diğer Mac’e aynen taşımak istersen `tts/comparison/private-session.json` ve `results/` klasörünü, aynı WAV/katalog dosyalarıyla birlikte özel olarak kopyala; Git’e ekleme. Sesleri yeniden üretirsen yeni bir kör oturum aç (`--state-dir tts/outputs/comparison-macbook`); eski sonuçlar korunur. Arayüz puanları iki cihaz arasında otomatik senkronize edilmez.

## Lisans ve ticari sosyal medya kullanımı

- **Antalia-2 Mini:** model kartı, LICENSE ve NOTICE kodu, normalizer’ı ve ağırlıkları Apache 2.0 olarak tanımlar. Ticari kullanım yasağı yok. Model/kod dağıtımında LICENSE/NOTICE ve ilgili atıfları koru. `cmudict` BSD 2-Clause bağımlılığıdır. Model sentetik eğitim sesinden üretilmiştir; model kartındaki AI sesi açıklama ve yanıltıcı kimlik kullanmama tavsiyesini koru.
- **EMA Lightning:** resmî kod lisansı ve model kartı Apache 2.0. Ticari içerik için lisans düzeyinde özel yasak yok; kod/model dağıtımında Apache bildirimleri korunur. `normalizer-tr` de Apache 2.0 olarak yayımlanmış bağımlılıktır.
- **Supertonic 3:** örnek kod MIT; **ağırlıklar OpenRAIL-M**. Ticari kullanıma genel bir yasak bulunmuyor, fakat kullanım kısıtları geçerli. Lisans §6 çıktıda hak talep etmez; çıktının kullanımından üretici sorumludur. Attachment A(e), üretilen içeriğin makine üretimi olduğunun açık ve anlaşılır biçimde açıklanmasını şart koşar. Bu adayla yayın yaparken yapay zekâ seslendirmesini açıklamak gerekir. Rızasız kimlik taklidi, zarar amaçlı yanlış bilgi, taciz, ayrımcılık ve diğer Attachment A kullanımları yasaktır; tıbbi tavsiye de kısıtlıdır. Ağırlık/model veya model hizmeti dağıtılırsa §4 kapsamındaki lisans, bildirim ve aşağıya aktarılan kısıtlar ayrıca uygulanır. Sadece “MIT” diye sınıflandırma.

Bunlar incelenen metinlerin uygulama açısından özeti; tam lisans kopyaları `licenses/` altında. Kanalın bilim anlatımı için belirlenen kullanımda genel ticari yasak saptanmadı; bu ifade her olası bölümün tüm haklarını garanti etmez. Herhangi bir üçüncü kişinin sesini klonlama veya kişiyi taklit etme yapılmadı.

## Kurulumda karşılaşılan durum

İlk proje içi indirici `uv 0.9.5`, 3.11.15 yönetilen Python indirmesini tanımıyordu. Üç modelin kurulumu zaten çalışıyordu; taşınabilir kurulum testi bu sorunu yakaladı. Sadece bootstrap ortamındaki uv 0.12.24’e yükseltildi; ardından sabit Python sürümleri indirilip üç kilit ve 29 varlık tekrar doğrulandı. Başarısız eski deneme logu/sonraki loglar yerel `tts/outputs/` altında; başka ortam değiştirilmedi.
