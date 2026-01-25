# YouTube Downloader & Converter (Mass & Parallel) 🚀

A powerful and fast tool to download YouTube videos, Shorts, and convert them to high-quality MP3 or MP4 format with metadata extraction.

## ✨ Fitur Unggulan

- **Parallel Batch Download**: Men-download hingga **3 video sekaligus** secara bersamaan.
- **Extreme Speed**: Menggunakan **16 fragment simultan** per video untuk memaksimalkan kecepatan internet Anda.
- **Support YouTube Shorts**: Secara otomatis men-download Shorts dalam format **MP4 kualitas terbaik**.
- **Auto MP3 Converter**: Konversi otomatis ke MP3 kualitas tinggi (192kbps).
- **Metadata Companion**: Setiap download menyertakan file `.txt` berisi **Judul, Tags, dan Caption/Deskripsi** asli.
- **Local Conversion**: Fitur untuk mengkonversi file audio/video lokal di folder `downloads` ke MP3.
- **Manual Single Download**: Bisa men-download satu URL secara manual melalui menu.

## 🚀 Cara Penggunaan

### 1. Persiapan Awal

Jalankan file:
`setup.bat`

Ini akan:

- Membuat environment Python (`venv`).
- Menginstall seluruh dependencies (`yt-dlp`, `colorama`, dll).
- Mengecek dan memastikan FFmpeg tersedia (penting untuk konversi).

### 2. Cara Download Massal

1. Masukkan daftar link YouTube ke file `youtube_urls.txt` (satu link per baris).
2. Jalankan file:
   `download.bat`
3. Pilih menu yang diinginkan:
   - **Menu 1**: Batch Download ke **MP3** (Default).
   - **Menu 2**: Batch Download ke **MP4 (Shorts)**.
   - **Menu 3**: Download **Single URL** (Input manual).
4. Hasil file media dan metadata akan tersimpan di folder `downloads`.

### 3. Konversi Lokal

Jika Anda memiliki file di folder `downloads` yang belum menjadi MP3, gunakan **Menu 4** untuk mengkonversi semuanya secara otomatis.

## 🛠 Persyaratan

- **Python 3.8+**
- **FFmpeg** (Otomatis dicek oleh script)
- **Internet Speed**: Direkomendasikan internet stabil untuk mode parallel.

## 📝 Catatan

Script ini menggunakan `yt-dlp` yang sangat handal. Jika terjadi error, pastikan untuk menjalankan `setup.bat` ulang untuk memperbarui library.
