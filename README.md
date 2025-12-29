# YouTube MP3 Downloader Massal

Download video YouTube dan konversi otomatis ke MP3 kualitas tinggi (320kbps).

## Fitur

- Download massal dari file text
- Konversi otomatis ke MP3
- Kualitas Audio Terbaik (320kbps)
- Metadata otomatis
- Fitur konversi file lokal

## Cara Penggunaan

### 1. Setup Pertama Kali

Jalankan file:
`setup.bat`

Ini akan:

- Membuat environment Python
- Menginstall dependencies
- Mengecek/Menginstall FFmpeg (diperlukan untuk konversi MP3)

### 2. Cara Download

1. Masukkan link YouTube ke file `youtube_urls.txt` (satu link per baris).
2. Jalankan file:
   `download.bat`
3. Pilih menu "1" untuk mulai download.
4. File MP3 akan tersimpan di folder `downloads`.

### Menu Tambahan

Script `download.bat` juga memiliki fitur untuk mengkonversi file audio yang sudah ada di folder `downloads` jika sebelumnya gagal terkonversi.

## Persyaratan

- Python 3.8 atau lebih baru
- Koneksi Internet
