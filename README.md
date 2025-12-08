# 🎵 YouTube MP3 Downloader - Batch Download

Aplikasi untuk mendownload MP3 dari video YouTube secara masal dengan kualitas terbaik (320kbps).

## ✨ Fitur

- ✅ Download MP3 dengan kualitas maksimal (320kbps)
- ✅ Batch download dari file .txt
- ✅ Progress tracking untuk setiap video
- ✅ Error handling otomatis (skip video yang gagal)
- ✅ Tampilan CLI yang menarik dengan warna
- ✅ Ringkasan statistik download
- ✅ Cross-platform (Windows, Linux, macOS)
- ✅ Virtual environment untuk isolasi dependencies

## 📋 Persyaratan

- Python 3.7 atau lebih baru
- FFmpeg (untuk konversi audio)

## 🚀 Instalasi

### Metode 1: Otomatis (Recommended untuk Windows) ⭐

#### 1. Setup Virtual Environment & Dependencies

Double-click atau jalankan:

```bash
setup.bat
```

Script ini akan:

- Membuat virtual environment
- Install semua dependencies Python
- Memberikan instruksi install FFmpeg

#### 2. Install FFmpeg

Double-click atau jalankan:

```bash
install-ffmpeg.bat
```

Script ini akan mencoba install FFmpeg otomatis menggunakan winget.

**Jika gagal**, install manual:

1. Download dari: https://www.gyan.dev/ffmpeg/builds/
2. Extract ke folder (misal: `C:\ffmpeg`)
3. Tambahkan `C:\ffmpeg\bin` ke PATH
4. Restart terminal

#### 3. Jalankan Aplikasi

Double-click atau jalankan:

```bash
run.bat
```

---

### Metode 2: Manual

#### 1. Install Python

Pastikan Python sudah terinstall. Cek dengan:

```bash
python --version
```

#### 2. Buat Virtual Environment

```bash
python -m venv venv
```

#### 3. Aktifkan Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

#### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 5. Install FFmpeg

**Windows (winget):**

```bash
winget install ffmpeg
```

**Windows (Chocolatey - Run as Admin):**

```bash
choco install ffmpeg
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**

```bash
brew install ffmpeg
```

## 📖 Cara Penggunaan

### 1. Siapkan File URL

Buat atau edit file `youtube_urls.txt` dan masukkan URL YouTube (satu per baris):

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://www.youtube.com/watch?v=jNQXAC9IVRw
https://www.youtube.com/watch?v=9bZkp7q19f0
```

### 2. Jalankan Aplikasi

**Metode 1 (Recommended):**

```bash
run.bat
```

**Metode 2 (Manual):**

```bash
# Aktifkan virtual environment terlebih dahulu
venv\Scripts\activate

# Jalankan aplikasi
python downloader.py
```

### 3. Ikuti Instruksi

- Tekan ENTER untuk menggunakan default settings
- Atau masukkan custom path untuk file URL dan folder output
- Konfirmasi untuk memulai download

### 4. Hasil Download

File MP3 akan tersimpan di folder `downloads/` (atau folder custom yang Anda tentukan)

## 🎯 Contoh Output

```
╔════════════════════════════════════════════════════════════════════╗
║         🎵 YOUTUBE MP3 DOWNLOADER - KUALITAS TERBAIK 🎵          ║
╚════════════════════════════════════════════════════════════════════╝

Tekan ENTER untuk menggunakan nilai default

File URL (.txt) [youtube_urls.txt]:
Folder output [downloads]:

✓ Berhasil membaca 3 URL dari youtube_urls.txt

======================================================================
🎵 YOUTUBE MP3 DOWNLOADER - BATCH MODE 🎵
======================================================================
Total video: 3
Output folder: C:\Users\Dev\Desktop\app-downloader-mp3\downloads
Kualitas: 320kbps (Maksimal)

======================================================================
[1/3] Memproses: https://www.youtube.com/watch?v=dQw4w9WgXcQ
======================================================================

[download] Downloading video...
[download] 100% of 3.5MiB in 00:02
[ffmpeg] Correcting container in "Rick Astley - Never Gonna Give You Up.m4a"
[ffmpeg] Destination: Rick Astley - Never Gonna Give You Up.mp3

✓ Berhasil mendownload [1/3]

...

======================================================================
📊 RINGKASAN DOWNLOAD 📊
======================================================================
✓ Berhasil: 3/3
✗ Gagal: 0/3
📁 Lokasi file: C:\Users\Dev\Desktop\app-downloader-mp3\downloads
======================================================================
```

## ⚙️ Konfigurasi Lanjutan

### Mengubah Kualitas Audio

Edit `downloader.py` pada bagian `ydl_opts`:

```python
'preferredquality': '320',  # Ubah ke '192' atau '128' untuk ukuran lebih kecil
```

### Mengubah Format Output

```python
'preferredcodec': 'mp3',  # Ubah ke 'opus', 'wav', 'm4a', dll
```

### Custom Output Template

```python
'outtmpl': str(self.output_folder / '%(artist)s - %(title)s.%(ext)s'),
```

## 🔧 Troubleshooting

### Error: "FFmpeg not found"

**Solusi:** Install FFmpeg dan pastikan ada di PATH system

### Error: "Unable to extract video data"

**Solusi:**

- Pastikan URL valid
- Cek koneksi internet
- Video mungkin private atau restricted

### Download sangat lambat

**Solusi:**

- Cek koneksi internet
- Beberapa video memiliki ukuran besar
- Gunakan kualitas lebih rendah jika perlu

### File tidak muncul di folder downloads

**Solusi:**

- Cek console untuk error messages
- Pastikan ada permission write ke folder
- Cek apakah FFmpeg terinstall dengan benar

### Error: "ModuleNotFoundError"

**Solusi:**

- Pastikan virtual environment sudah diaktifkan
- Jalankan `pip install -r requirements.txt`
- Atau gunakan `setup.bat` untuk setup otomatis

## 📝 Tips

1. **Kualitas vs Ukuran File:**

   - 320kbps: Kualitas terbaik, ukuran ~3-5MB per menit
   - 192kbps: Kualitas bagus, ukuran ~2-3MB per menit
   - 128kbps: Kualitas standar, ukuran ~1-2MB per menit

2. **Batch Download Besar:**

   - Untuk 100+ video, pertimbangkan split ke beberapa file
   - Monitor disk space
   - Gunakan `ignoreerrors: True` untuk skip video bermasalah

3. **Playlist YouTube:**
   - Bisa langsung paste URL playlist
   - Atau gunakan `yt-dlp` command untuk extract URLs dulu

## 📁 Struktur File

```
app-downloader-mp3/
├── downloader.py          # Script utama
├── requirements.txt       # Dependencies Python
├── youtube_urls.txt       # File input URL
├── setup.bat             # Setup otomatis (Windows)
├── run.bat               # Jalankan aplikasi (Windows)
├── install-ffmpeg.bat    # Install FFmpeg (Windows)
├── venv/                 # Virtual environment (dibuat otomatis)
├── downloads/            # Folder output MP3 (dibuat otomatis)
└── README.md             # Dokumentasi
```

## 📄 Lisensi

MIT License - Bebas digunakan untuk keperluan pribadi maupun komersial

## 🤝 Kontribusi

Silakan buat issue atau pull request untuk improvement!

## ⚠️ Disclaimer

Aplikasi ini hanya untuk keperluan pribadi. Pastikan Anda memiliki hak untuk mendownload konten yang Anda download. Hormati hak cipta creator.
