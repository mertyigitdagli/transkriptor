# SES TRANSKRİPSİYON ARACI
## Whisper AI ile Ses Dosyalarını Metne Dönüştürme

---

## GENEL BAKIŞ

Bu araç, ses ve video dosyalarını otomatik olarak metne dönüştürür (transkribe eder).
OpenAI'nin Whisper AI teknolojisini kullanır ve tamamen ücretsizdir.

**Özellikler:**
- ✅ Tamamen offline çalışır (internet gerekmez)
- ✅ 100+ dil desteği (Türkçe dahil)
- ✅ Sınırsız kullanım
- ✅ Toplu dosya işleme
- ✅ Zaman damgalı çıktı
- ✅ SRT altyazı formatı desteği
- ✅ Yüksek doğruluk oranı

---

## KURULUM

### Adım 1: Python Kurulumu
Python 3.8 veya üzeri gereklidir.
İndirmek için: https://www.python.org/downloads/

### Adım 2: Gerekli Paketleri Yükleyin
Komut satırını açın ve şu komutları çalıştırın:

```bash
pip install openai-whisper
pip install torch
```

**Not:** İlk kurulum 500MB-1GB indirme gerektirebilir.

### Adım 3: Script'i İndirin
`transkript.py` dosyasını bir klasöre kaydedin.

---

## KULLANIM

### Temel Kullanım

```bash
python transkript.py -i DOSYA_YOLU -o CIKTI_KLASORU
```

### Örnekler

**1. Tek bir ses dosyasını transkribe et:**
```bash
python transkript.py -i ses.mp3 -o transkriptler/
```

**2. Klasördeki tüm ses dosyalarını işle:**
```bash
python transkript.py -i ses_klasoru/ -o transkriptler/
```

**3. Türkçe ses için (önerilen):**
```bash
python transkript.py -i ses.mp3 -o transkriptler/ -l tr
```

**4. Zaman damgalı transkript oluştur:**
```bash
python transkript.py -i ses.mp3 -o transkriptler/ -t
```

**5. Daha yüksek kalite (daha yavaş):**
```bash
python transkript.py -i ses.mp3 -o transkriptler/ -s medium
```

**6. Tüm seçenekler birlikte:**
```bash
python transkript.py -i ses_klasoru/ -o transkriptler/ -l tr -s medium -t
```

---

## PARAMETRELERİN AÇIKLAMASI

### Zorunlu Parametreler:
- `-i, --input`: Ses dosyası veya klasör yolu
- `-o, --output`: Transkriptlerin kaydedileceği klasör

### Opsiyonel Parametreler:

**-s, --model-size** (Model boyutu)
- `tiny` - En hızlı, düşük doğruluk (~1GB RAM, 32x daha hızlı)
- `base` - Dengeli (Varsayılan) (~1GB RAM)
- `small` - İyi doğruluk (~2GB RAM)
- `medium` - Yüksek doğruluk (~5GB RAM) **[ÖNERİLEN]**
- `large` - En yüksek doğruluk (~10GB RAM, en yavaş)

**-l, --language** (Dil kodu)
- Örnek: `tr` (Türkçe), `en` (İngilizce), `de` (Almanca)
- Belirtilmezse otomatik tespit edilir
- Dil belirtmek doğruluğu artırır

**-t, --timestamps** (Zaman damgaları)
- Transkripte zaman bilgisi ekler
- SRT altyazı dosyası oluşturur
- Video editörleri ile uyumlu

---

## DESTEKLENEN DOSYA FORMATLARI

**Ses Formatları:**
- MP3
- WAV
- M4A
- OGG
- FLAC
- AAC
- WMA

**Video Formatları:**
- MP4 (sadece ses kısmı işlenir)

---

## ÇIKTI DOSYALARI

Script iki tip dosya oluşturur:

### 1. Metin Dosyası (.txt)
```
Dosya: ornek_ses.mp3
Tarih: 2024-12-08 14:30:00
Tespit edilen dil: tr
================================================================================

=== ZAMAN DAMGALI TRANSKRİPT === (opsiyonel)

[00:00:00 - 00:00:05] Merhaba, bu bir test kaydıdır.
[00:00:05 - 00:00:10] Whisper AI kullanarak transkripsiyon yapıyoruz.

================================================================================

=== TAM METİN ===

Merhaba, bu bir test kaydıdır. Whisper AI kullanarak transkripsiyon yapıyoruz.
```

### 2. SRT Altyazı Dosyası (.srt) - Sadece -t parametresi ile
```
1
00:00:00,000 --> 00:00:05,000
Merhaba, bu bir test kaydıdır.

2
00:00:05,000 --> 00:00:10,000
Whisper AI kullanarak transkripsiyon yapıyoruz.
```

---

## PERFORMANS İPUÇLARI

### Model Seçimi:
- **Hızlı işlem için:** `tiny` veya `base`
- **Kalite-hız dengesi:** `small`
- **En iyi sonuç:** `medium` (önerilen)
- **Profesyonel kullanım:** `large`

### İşlem Süreleri (yaklaşık):
- **tiny**: 1 dakikalık ses = ~5 saniye
- **base**: 1 dakikalık ses = ~10 saniye
- **small**: 1 dakikalık ses = ~20 saniye
- **medium**: 1 dakikalık ses = ~40 saniye
- **large**: 1 dakikalık ses = ~2 dakika

**Not:** Süreler bilgisayar donanımına göre değişir.

### Bellek Gereksinimleri:
- tiny/base: 1-2 GB RAM
- small: 2-3 GB RAM
- medium: 5-6 GB RAM
- large: 10+ GB RAM

---

## SORUN GİDERME

### "openai-whisper paketi yüklü değil" hatası:
```bash
pip install openai-whisper
```

### "torch" hatası:
```bash
pip install torch
```

### Model indirilemiyor:
İnternet bağlantınızı kontrol edin. İlk kullanımda model indirilmesi gerekir.

### Ses dosyası işlenmiyor:
- Dosya formatının desteklendiğinden emin olun
- Dosya yolunda Türkçe karakter varsa İngilizce karakterle değiştirin
- Dosyanın bozuk olmadığından emin olun

### Çok yavaş çalışıyor:
- Daha küçük bir model kullanın (`-s tiny` veya `-s base`)
- GPU desteği için CUDA yükleyin (opsiyonel, ileri seviye)

### Yanlış dil tespit ediliyor:
Dil parametresini açıkça belirtin: `-l tr`

---

## DİL KODLARI

Yaygın kullanılan dil kodları:

- `tr` - Türkçe
- `en` - İngilizce
- `de` - Almanca
- `fr` - Fransızca
- `es` - İspanyolca
- `it` - İtalyanca
- `pt` - Portekizce
- `ru` - Rusça
- `zh` - Çince
- `ja` - Japonca
- `ko` - Korece
- `ar` - Arapça

Toplam 100+ dil desteklenmektedir.

---

## ÖRNEK KULLANIM SENARYOLARı

### Senaryo 1: Podcast Transkribe Etme
```bash
python transkript.py -i podcast.mp3 -o transkriptler/ -l tr -s medium -t
```

### Senaryo 2: Toplantı Kaydı
```bash
python transkript.py -i toplanti.m4a -o toplanti_notlari/ -l tr -s small
```

### Senaryo 3: Video Altyazısı Oluşturma
```bash
python transkript.py -i video.mp4 -o altyazilar/ -l tr -s medium -t
```

### Senaryo 4: Toplu Dosya İşleme
```bash
python transkript.py -i ses_arsivi/ -o tum_transkriptler/ -l tr -s base
```

---

## SIK SORULAN SORULAR

**S: İnternet bağlantısı gerekli mi?**
C: Sadece ilk kurulum sırasında. Sonrasında tamamen offline çalışır.

**S: Ücretli mi?**
C: Hayır, tamamen ücretsiz ve açık kaynak.

**S: Kaç dakikalık ses işleyebilir?**
C: Sınır yok. Saatlerce ses işleyebilir.

**S: Doğruluk oranı ne kadar?**
C: Kaliteli kayıtlarda %90-95. Gürültülü kayıtlarda %70-85.

**S: GPU gerekli mi?**
C: Hayır, CPU ile de çalışır. GPU varsa daha hızlı olur.

**S: Mac/Linux'ta çalışır mı?**
C: Evet, Windows, Mac ve Linux desteklenir.

---

## TEKNİK DETAYLAR

**Kullanılan Teknoloji:** OpenAI Whisper
**Lisans:** MIT (Açık Kaynak)
**Python Versiyonu:** 3.8+
**Ana Bağımlılıklar:**
- openai-whisper
- torch
- numpy
- ffmpeg (otomatik yüklenir)

---

## DESTEK VE GÜNCELLEMELER

**Whisper Resmi Deposu:**
https://github.com/openai/whisper

**Python Resmi Sitesi:**
https://www.python.org/

---

## LİSANS

Bu script MIT lisansı altında dağıtılmaktadır.
OpenAI Whisper'ın lisansı için: https://github.com/openai/whisper/blob/main/LICENSE

---

## YAYIN TARİHİ

Aralık 2024

---

## HIZLI BAŞLANGIÇ ÖZETİ

1. Python yükleyin
2. `pip install openai-whisper` çalıştırın
3. `python transkript.py -i ses.mp3 -o ciktilar/ -l tr` komutu ile başlayın
4. Sonuçları `ciktilar/` klasöründe bulun

İyi kullanımlar! 🎙️✨