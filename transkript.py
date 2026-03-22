import os
import argparse
from pathlib import Path
from datetime import datetime

def transcribe_audio(audio_path, model_size="base", language=None):
    """Whisper modeli kullanarak transkripsiyon"""
    try:
        import whisper
        
        print(f"Model yükleniyor: {model_size}")
        model = whisper.load_model(model_size)
        
        params = {"fp16": False, "verbose": False}
        if language:
            params["language"] = language
        
        print("Transkripsiyon yapılıyor...")
        result = model.transcribe(str(audio_path), **params)
        
        return {
            "text": result["text"],
            "segments": result.get("segments", []),
            "language": result.get("language", "unknown")
        }
    except ImportError:
        print("\n❌ HATA: 'openai-whisper' paketi yüklü değil!")
        print("\nKurulum için şu komutları çalıştırın:")
        print("  pip install openai-whisper")
        print("  pip install setuptools-rust  # (gerekirse)")
        return None
    except Exception as e:
        print(f"\n❌ Hata: {str(e)}")
        return None

def format_timestamp(seconds):
    """Saniyeyi HH:MM:SS formatına çevir"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def save_transcript(result, audio_file, output_dir, include_timestamps=False):
    """Transkripti dosyaya kaydet"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Basit metin dosyası
    output_file = output_dir / f"{audio_file.stem}_transcript.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Dosya: {audio_file.name}\n")
        f.write(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Tespit edilen dil: {result['language']}\n")
        f.write("=" * 80 + "\n\n")
        
        if include_timestamps and result['segments']:
            f.write("=== ZAMAN DAMGALI TRANSKRİPT ===\n\n")
            for segment in result['segments']:
                start = format_timestamp(segment['start'])
                end = format_timestamp(segment['end'])
                text = segment['text'].strip()
                f.write(f"[{start} - {end}] {text}\n")
            f.write("\n" + "=" * 80 + "\n\n")
        
        f.write("=== TAM METİN ===\n\n")
        f.write(result['text'].strip())
    
    print(f"✓ Kaydedildi: {output_file.name}")
    
    # SRT formatında da kaydet (opsiyonel)
    if include_timestamps and result['segments']:
        srt_file = output_dir / f"{audio_file.stem}_transcript.srt"
        with open(srt_file, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(result['segments'], 1):
                start = format_timestamp(segment['start']).replace('.', ',')
                end = format_timestamp(segment['end']).replace('.', ',')
                text = segment['text'].strip()
                f.write(f"{i}\n")
                f.write(f"{start},000 --> {end},000\n")
                f.write(f"{text}\n\n")
        print(f"✓ SRT kaydedildi: {srt_file.name}")

def process_audio_files(input_path, output_dir, model_size="base", language=None, 
                       include_timestamps=False):
    """Ses dosyalarını işle ve transkribe et"""
    input_path = Path(input_path)
    
    # Desteklenen ses formatları
    audio_extensions = {'.mp3', '.wav', '.m4a', '.ogg', '.flac', '.aac', '.wma', '.mp4'}
    
    # Dosya veya klasör kontrolü
    if input_path.is_file():
        if input_path.suffix.lower() in audio_extensions:
            audio_files = [input_path]
        else:
            print(f"❌ Desteklenmeyen dosya formatı: {input_path.suffix}")
            return
    else:
        audio_files = [f for f in input_path.rglob('*') if f.suffix.lower() in audio_extensions]
    
    if not audio_files:
        print("❌ Hiç ses dosyası bulunamadı!")
        print(f"Desteklenen formatlar: {', '.join(audio_extensions)}")
        return
    
    print(f"\n{'='*80}")
    print(f"Toplam {len(audio_files)} ses dosyası bulundu")
    print(f"Model: {model_size}")
    print(f"Dil: {language if language else 'Otomatik tespit'}")
    print(f"{'='*80}\n")
    
    # Model bir kere yüklensin (performans için)
    try:
        import whisper
        print(f"Model yükleniyor: {model_size}")
        model = whisper.load_model(model_size)
        print("✓ Model yüklendi\n")
    except Exception as e:
        print(f"❌ Model yüklenemedi: {e}")
        return
    
    successful = 0
    failed = 0
    
    for i, audio_file in enumerate(audio_files, 1):
        print(f"\n[{i}/{len(audio_files)}] İşleniyor: {audio_file.name}")
        print("-" * 80)
        
        try:
            # Transkripsiyon yap
            params = {"fp16": False, "verbose": False}
            if language:
                params["language"] = language
            
            result = model.transcribe(str(audio_file), **params)
            
            result_dict = {
                "text": result["text"],
                "segments": result.get("segments", []),
                "language": result.get("language", "unknown")
            }
            
            # Sonuçları kaydet
            save_transcript(result_dict, audio_file, output_dir, include_timestamps)
            successful += 1
            
        except Exception as e:
            print(f"❌ Hata: {str(e)}")
            failed += 1
    
    # Özet
    print(f"\n{'='*80}")
    print(f"İşlem tamamlandı!")
    print(f"✓ Başarılı: {successful}")
    if failed > 0:
        print(f"❌ Başarısız: {failed}")
    print(f"{'='*80}\n")

def main():
    parser = argparse.ArgumentParser(
        description="Ses dosyalarını metne dönüştürür (Whisper AI kullanarak)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
KURULUM:
  pip install openai-whisper torch

ÖRNEKLER:
  # Tek dosya transkribe et
  python script.py -i ses.mp3 -o transkriptler/
  
  # Klasördeki tüm dosyalar
  python script.py -i ses_klasoru/ -o transkriptler/
  
  # Türkçe dil belirtimi
  python script.py -i ses.mp3 -o transkriptler/ -l tr
  
  # Zaman damgalı transkript
  python script.py -i ses.mp3 -o transkriptler/ -t
  
  # Daha yüksek doğruluk (daha yavaş)
  python script.py -i ses.mp3 -o transkriptler/ -s medium

MODEL BOYUTLARI:
  tiny   - En hızlı, düşük doğruluk (~1GB RAM)
  base   - Dengeli (varsayılan) (~1GB RAM)
  small  - İyi doğruluk (~2GB RAM)
  medium - Yüksek doğruluk (~5GB RAM)
  large  - En yüksek doğruluk (~10GB RAM)

DİL KODLARI:
  tr - Türkçe
  en - İngilizce
  de - Almanca
  fr - Fransızca
  es - İspanyolca
  (Belirtilmezse otomatik tespit edilir)
        """
    )
    
    parser.add_argument('-i', '--input', required=True,
                       help='Ses dosyası veya klasör yolu')
    parser.add_argument('-o', '--output', required=True,
                       help='Transkriptlerin kaydedileceği klasör')
    parser.add_argument('-s', '--model-size', 
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       default='base',
                       help='Whisper model boyutu (varsayılan: base)')
    parser.add_argument('-l', '--language',
                       help='Ses dili kodu (örn: tr, en, de) - Opsiyonel')
    parser.add_argument('-t', '--timestamps', action='store_true',
                       help='Zaman damgalı transkript oluştur (SRT dahil)')
    
    args = parser.parse_args()
    
    # İşlemi başlat
    process_audio_files(
        args.input,
        args.output,
        model_size=args.model_size,
        language=args.language,
        include_timestamps=args.timestamps
    )

if __name__ == "__main__":
    main()