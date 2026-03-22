import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from pathlib import Path
from datetime import datetime
import queue

class TranskriptorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Transkriptor - Ses Transkripsiyon Aracı")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Değişkenler
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar(value="transkriptler")
        self.model_size = tk.StringVar(value="base")
        self.language = tk.StringVar(value="tr")
        self.timestamps = tk.BooleanVar(value=False)
        self.is_processing = False
        self.log_queue = queue.Queue()
        
        self.setup_ui()
        self.check_dependencies()
        self.process_log_queue()
        
    def setup_ui(self):
        # Ana container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Başlık
        title_label = ttk.Label(main_frame, text="🎙️ Transkriptor", 
                               font=("Arial", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, 
                                   text="Ses dosyalarını metne dönüştürün",
                                   font=("Arial", 10))
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Dosya Seçimi Bölümü
        input_frame = ttk.LabelFrame(main_frame, text="📁 Giriş", padding="10")
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(input_frame, text="Ses Dosyası/Klasör:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.input_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(input_frame, text="Dosya Seç", command=self.select_file).grid(row=0, column=2, padx=2, pady=5)
        ttk.Button(input_frame, text="Klasör Seç", command=self.select_folder).grid(row=0, column=3, padx=2, pady=5)
        
        # Çıktı Klasörü
        ttk.Label(input_frame, text="Çıktı Klasörü:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.output_path, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(input_frame, text="Klasör Seç", command=self.select_output).grid(row=1, column=2, columnspan=2, pady=5)
        
        # Ayarlar Bölümü
        settings_frame = ttk.LabelFrame(main_frame, text="⚙️ Ayarlar", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Model Boyutu
        ttk.Label(settings_frame, text="Model Boyutu:").grid(row=0, column=0, sticky=tk.W, pady=5)
        model_combo = ttk.Combobox(settings_frame, textvariable=self.model_size, 
                                   values=["tiny", "base", "small", "medium", "large"],
                                   state="readonly", width=15)
        model_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(settings_frame, text="(base: Hızlı, medium: Kaliteli)").grid(row=0, column=2, sticky=tk.W, padx=5)
        
        # Dil
        ttk.Label(settings_frame, text="Dil:").grid(row=1, column=0, sticky=tk.W, pady=5)
        lang_combo = ttk.Combobox(settings_frame, textvariable=self.language,
                                 values=["tr", "en", "de", "fr", "es", "it", "pt", "ru", "ar"],
                                 state="readonly", width=15)
        lang_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(settings_frame, text="(tr: Türkçe, en: İngilizce)").grid(row=1, column=2, sticky=tk.W, padx=5)
        
        # Zaman Damgası
        ttk.Checkbutton(settings_frame, text="Zaman damgalı transkript oluştur (SRT dahil)", 
                       variable=self.timestamps).grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=10)
        
        # İşlem Butonu
        self.process_button = ttk.Button(main_frame, text="▶️ Transkripte Başla", 
                                        command=self.start_transcription,
                                        style="Accent.TButton")
        self.process_button.grid(row=4, column=0, columnspan=3, pady=20, ipadx=20, ipady=10)
        
        # İlerleme Bölümü
        progress_frame = ttk.LabelFrame(main_frame, text="📊 İlerleme", padding="10")
        progress_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, length=700)
        self.progress_bar.grid(row=0, column=0, pady=5, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(progress_frame, text="Hazır", 
                                     font=("Arial", 9))
        self.status_label.grid(row=1, column=0, pady=5)
        
        # Log Bölümü
        log_frame = ttk.LabelFrame(main_frame, text="📝 Günlük", padding="10")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=90, 
                                                  font=("Consolas", 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        progress_frame.columnconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
    def check_dependencies(self):
        """Whisper kurulu mu kontrol et"""
        try:
            import whisper
            self.log("✓ Whisper kütüphanesi hazır")
        except ImportError:
            self.log("❌ Whisper kütüphanesi bulunamadı!")
            self.log("Kurulum için: pip install openai-whisper")
            messagebox.showerror("Hata", 
                               "Whisper kütüphanesi yüklü değil!\n\n"
                               "Lütfen şu komutu çalıştırın:\n"
                               "pip install openai-whisper")
    
    def select_file(self):
        filename = filedialog.askopenfilename(
            title="Ses Dosyası Seç",
            filetypes=[
                ("Ses Dosyaları", "*.mp3 *.wav *.m4a *.ogg *.flac *.aac"),
                ("Tüm Dosyalar", "*.*")
            ]
        )
        if filename:
            self.input_path.set(filename)
            self.log(f"Dosya seçildi: {os.path.basename(filename)}")
    
    def select_folder(self):
        foldername = filedialog.askdirectory(title="Klasör Seç")
        if foldername:
            self.input_path.set(foldername)
            self.log(f"Klasör seçildi: {foldername}")
    
    def select_output(self):
        foldername = filedialog.askdirectory(title="Çıktı Klasörü Seç")
        if foldername:
            self.output_path.set(foldername)
            self.log(f"Çıktı klasörü: {foldername}")
    
    def log(self, message):
        """Thread-safe logging"""
        self.log_queue.put(message)
    
    def process_log_queue(self):
        """Process log messages from queue"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_log_queue)
    
    def update_status(self, message):
        self.status_label.config(text=message)
    
    def start_transcription(self):
        if self.is_processing:
            messagebox.showwarning("Uyarı", "Zaten bir işlem devam ediyor!")
            return
        
        if not self.input_path.get():
            messagebox.showerror("Hata", "Lütfen bir ses dosyası veya klasör seçin!")
            return
        
        self.is_processing = True
        self.process_button.config(state="disabled", text="⏳ İşleniyor...")
        self.progress_var.set(0)
        
        # Thread'de çalıştır
        thread = threading.Thread(target=self.transcribe_worker, daemon=True)
        thread.start()
    
    def transcribe_worker(self):
        try:
            import whisper
            
            input_path = Path(self.input_path.get())
            output_dir = Path(self.output_path.get())
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Dosyaları bul
            audio_extensions = {'.mp3', '.wav', '.m4a', '.ogg', '.flac', '.aac', '.wma', '.mp4'}
            
            if input_path.is_file():
                if input_path.suffix.lower() in audio_extensions:
                    audio_files = [input_path]
                else:
                    self.log(f"❌ Desteklenmeyen dosya formatı: {input_path.suffix}")
                    self.finish_processing()
                    return
            else:
                audio_files = [f for f in input_path.rglob('*') if f.suffix.lower() in audio_extensions]
            
            if not audio_files:
                self.log("❌ Hiç ses dosyası bulunamadı!")
                self.finish_processing()
                return
            
            total_files = len(audio_files)
            self.log(f"\n{'='*60}")
            self.log(f"Toplam {total_files} dosya bulundu")
            self.log(f"Model: {self.model_size.get()}")
            self.log(f"Dil: {self.language.get()}")
            self.log(f"{'='*60}\n")
            
            # Model yükle
            self.update_status("Model yükleniyor...")
            self.log("Model yükleniyor...")
            model = whisper.load_model(self.model_size.get())
            self.log("✓ Model yüklendi\n")
            
            # Her dosyayı işle
            successful = 0
            for i, audio_file in enumerate(audio_files, 1):
                try:
                    self.log(f"[{i}/{total_files}] İşleniyor: {audio_file.name}")
                    self.update_status(f"İşleniyor: {audio_file.name} ({i}/{total_files})")
                    
                    # İlerleme
                    progress = (i / total_files) * 100
                    self.progress_var.set(progress)
                    
                    # Transkripsiyon
                    params = {"fp16": False, "verbose": False}
                    if self.language.get():
                        params["language"] = self.language.get()
                    
                    result = model.transcribe(str(audio_file), **params)
                    
                    # Kaydet
                    self.save_transcript(result, audio_file, output_dir)
                    self.log(f"✓ Tamamlandı: {audio_file.name}\n")
                    successful += 1
                    
                except Exception as e:
                    self.log(f"❌ Hata: {str(e)}\n")
            
            # Özet
            self.log(f"\n{'='*60}")
            self.log(f"İşlem tamamlandı!")
            self.log(f"✓ Başarılı: {successful}/{total_files}")
            self.log(f"Çıktı klasörü: {output_dir}")
            self.log(f"{'='*60}\n")
            
            self.progress_var.set(100)
            self.update_status("Tamamlandı!")
            
            messagebox.showinfo("Başarılı", 
                              f"Transkripsiyon tamamlandı!\n\n"
                              f"Başarılı: {successful}/{total_files}\n"
                              f"Çıktı: {output_dir}")
            
        except Exception as e:
            self.log(f"\n❌ Kritik Hata: {str(e)}")
            messagebox.showerror("Hata", f"Bir hata oluştu:\n{str(e)}")
        
        finally:
            self.finish_processing()
    
    def save_transcript(self, result, audio_file, output_dir):
        """Transkripti kaydet"""
        output_file = output_dir / f"{audio_file.stem}_transcript.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Dosya: {audio_file.name}\n")
            f.write(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Tespit edilen dil: {result.get('language', 'unknown')}\n")
            f.write("=" * 80 + "\n\n")
            
            if self.timestamps.get() and result.get('segments'):
                f.write("=== ZAMAN DAMGALI TRANSKRİPT ===\n\n")
                for segment in result['segments']:
                    start = self.format_timestamp(segment['start'])
                    end = self.format_timestamp(segment['end'])
                    text = segment['text'].strip()
                    f.write(f"[{start} - {end}] {text}\n")
                f.write("\n" + "=" * 80 + "\n\n")
                
                # SRT kaydet
                srt_file = output_dir / f"{audio_file.stem}_transcript.srt"
                with open(srt_file, 'w', encoding='utf-8') as sf:
                    for i, segment in enumerate(result['segments'], 1):
                        start = self.format_timestamp(segment['start']).replace('.', ',')
                        end = self.format_timestamp(segment['end']).replace('.', ',')
                        text = segment['text'].strip()
                        sf.write(f"{i}\n")
                        sf.write(f"{start},000 --> {end},000\n")
                        sf.write(f"{text}\n\n")
            
            f.write("=== TAM METİN ===\n\n")
            f.write(result['text'].strip())
    
    def format_timestamp(self, seconds):
        """Saniyeyi HH:MM:SS formatına çevir"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def finish_processing(self):
        self.is_processing = False
        self.process_button.config(state="normal", text="▶️ Transkripte Başla")
        if self.progress_var.get() != 100:
            self.update_status("Hazır")

def main():
    root = tk.Tk()
    app = TranskriptorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()