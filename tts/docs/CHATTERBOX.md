# İsteğe bağlı yerel Chatterbox Multilingual V3

10 Ekim 2026, Apple Silicon Mac. Açık kullanıcı isteğiyle ayrı model kuruldu. Supertonic 3/M1, Antalia-2 Mini, merkezi anlatıcı seçimi ve eski videolar korunur. Yeni aday bölüm: `solar-basketball-chatterbox-tr`.

## Sabitlenmiş kaynaklar

- Kod: https://github.com/resemble-ai/chatterbox — `5de7a54aa4e5e2baadb0182dde554908b48b85c2`, paket 0.1.7.
- Ağırlık: https://huggingface.co/ResembleAI/chatterbox — `5bb1f6ee58e50c3b8d408bc82a6d3740c2db6e18`.
- V3 açıkça seçilir: `t3_mtl23ls_v3.safetensors`. Kütüphanenin varsayılanı V2 olabilir; varsayılan checkpoint'e güvenme.
- Ortam: Python 3.11.15; torch/torchaudio 2.6.0, transformers 5.2.0, diffusers 0.29.0, librosa 0.11.0. Tam kilit `tts/locks/chatterbox.txt`. Perth kaynağı da commit ile kilitlidir.
- 7 resmî dosya SHA-256: `tts/config/chatterbox-assets.json`; ayarlar/revision'lar `tts/config/chatterbox.json`.
- CPU, 4 thread; doğal 24 kHz mono FLOAT WAV. Bölüm içe aktarması 48 kHz PCM24 çalışma kopyası üretir. MPS kodda desteklenir; bu teslimin üretimi CPU'dur, MPS performansı doğrulanmış sayılmaz.
- Kod/model MIT: `tts/docs/licenses/chatterbox/LICENSE`. Ticari üretime uygun lisans; yeniden dağıtılan yazılımda telif/lisans bildirimlerini koru. Dışarıdan kişinin sesi alınmadı. İlk adaylar resmî `conds.pt` koşullandırmasıyla, son aday aşağıda belgelenen Türkçe proje referansıyla üretildi; kişi/aktör veya özel resmî profil adı uydurulmaz. Perth watermark korunur.

## Kurulum ve üretim

```sh
npm run tts:chatterbox:setup
npm run tts:chatterbox -- --text 'Güneş’i bir basketbol topu kadar küçültseydik…' \
  --output tts/outputs/chatterbox/yeni-ornek.wav
# Tam metin; çıktı mevcutsa hata verir.
npm run tts:chatterbox -- --text-file src/episodes/solar-basketball-chatterbox-tr/script.txt \
  --output tts/outputs/episodes/solar-basketball-chatterbox-tr/yeni-kayit.wav
```

Kurulum yalnız Chatterbox venv/vendor/weights alanlarını kullanır. Sistem Python'una paket kurulmaz. İlk kurulum internet gerektirir. Üretim `from_local` kullanır; HF offline bayrakları ve socket audit hook aktiftir. macOS'ta doğrulanan daha güçlü ağ yasağı:

```sh
/usr/bin/sandbox-exec -p '(version 1) (allow default) (deny network*)' \
  tts/environments/chatterbox/bin/python tts/adapters/chatterbox_v3.py \
  --text 'Dünya, bu ölçekte küçücük bir noktadır.' \
  --output tts/outputs/chatterbox/yeni-offline.wav
```

`--allow-network` yalnız kurulum tanısı içindir; normal ses üretiminde kullanılmaz. Model, venv, kaynak klonu, native WAV, chunk'lar ve cache Git dışıdır. İki Mac'te ortamlar yerelde yeniden kurulur.

## Türkçe için gerekli çevrimdışı uyumluluk

Resmî tokenizer, Türkçe kullanırken bile Çincedeki Cangjie/pkuseg yardımcısını ilk açılışta başlatıp ayrı bir model indirmeye çalışıyordu. İlk ağ yasağı testi bu yüzden durdu. Yalnız Türkçe çalışan adaptör, kullanılmayan `ChineseCangjieConverter` kurucusunu etkisiz hale getirir. Türkçe tokenizer yolu, ağırlıklar ve vendor kaynakları değiştirilmez. Adaptör başka diller için genel amaçlı olarak sunulmaz. Bu düzeltmeden sonra kısa ve tam üretim ağ yasağı altında çalıştırılır; gerçek sonuçlar üretim JSON'larında kayıtlıdır.

İlk geliştirmede adaptör dosyasının `chatterbox.py` adı Python paketini gölgeledi; `chatterbox_v3.py` olarak düzeltildi. Bunlar çözülmüş kurulum sorunlarıdır.

## Ses seçimi ve sınırı

İki kısa aday: `cfg_weight=0.3` ve `0`; ikisinde exaggeration 0.35, temperature 0.7. Yerel Türkçe wav2vec2 greedy metin tanısında normalize karakter benzerliği sırasıyla 0.956 / 0.975 çıktı. Daha nötr `cfg_weight=0` tam üretime seçildi; bu bir doğallık puanı veya insan dinlemesi değildir. Referans İngilizce aksanını azaltmak için resmî rehber de cfg=0 seçeneğini tarif eder: https://github.com/resemble-ai/chatterbox#original-chatterbox-tips.

Her cümle doğal hızda, seed42+indeks ile üretilir. Native WAV'lar değiştirilmeden birleştirilir; yapay hız/pitch değişimi, ek süre doldurma veya eski kaydı kopyalama yoktur. Cümle WAV'ları, metinler, başlangıç örnekleri, süreler ve üretim kaynakları JSON'a kaydedilir. İnsan dinlemesi ve Türkçe kelime doğruluğu yalnız bu sayısal tanıyla onaylanmış sayılmaz.


## Son tercih: Türkçe M1 referanslı Chatterbox

Üçüncü denemede mevcut, proje içinde üretilmiş Supertonic 3/M1 TEST A kaydı Türkçe ses referansı olarak kullanıldı (M1 yeniden çalıştırılmadı). Aynı kısa cümlede normalize karakter benzerliği 0,9937 oldu; yerleşik ses adaylarında 0,9560 / 0,9747 idi. Bu teknik tanı ve kullanıcının önceki M1 erkek ses tercihi doğrultusunda son üretim `cfg_weight=0.3`, exaggeration0.35, temperature0.7 ile yapıldı. Doğallık kazananı ilan edilmez; insan dinlemesi yapılmadı.

Referans `tts/voices/chatterbox/m1-turkish-reference.flac` olarak kayıpsız ve taşınabilir saklanır. Kaynak/ses hash'i, metin ve lisans kökeni yanındaki `reference.json` içindedir. Kaynak çıktı Supertonic modelinin BigScience Open RAIL-M kullanım şartlarına tabidir (`tts/docs/licenses/supertonic-3/LICENSE`); Chatterbox kod/ağırlıkları MIT olarak kalır. Eğitim/fine-tuning yapılmadı, ağırlıklar değiştirilmedi; kayıt yalnız çalışma anı koşullandırmasıdır. İnsan kaydı, ünlü/aktör sesi veya yeni bir Chatterbox resmî profil adı olarak sunulmaz.

Adaptör varsayılan olarak merkezi Chatterbox config'indeki bu referansı kullanır. Yerleşik aday için `--builtin-voice`, başka hakları uygun yerel kayıt için `--reference <dosya>` verilebilir. Supertonic merkezi anlatıcı config'i ayrı ve değişmemiştir. Yerleşik sesle üretilmiş68,8 s ilk tam aday ve hizalaması yerel `renders/episodes/solar-basketball-chatterbox/builtin-candidate` / `tts/outputs/episodes/solar-basketball-chatterbox` içinde korunur; nihai video ayrı `solar-basketball-chatterbox-tr` kimliğindedir.
