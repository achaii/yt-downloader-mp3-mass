# 🚀 Quick Start Guide

## Cara Tercepat Menggunakan Aplikasi

### 1️⃣ Aktifkan Virtual Environment

```bash
venv/Scripts/activate
```

### 2️⃣ Jalankan Aplikasi

```bash
python downloader.py
```

### 3️⃣ Ikuti Instruksi

- Tekan **ENTER** untuk default settings
- Ketik **y** untuk konfirmasi download

---

## 📝 Edit URL yang Akan Didownload

Buka file `youtube_urls.txt` dan masukkan URL YouTube (satu per baris):

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://www.youtube.com/watch?v=jNQXAC9IVRw
https://www.youtube.com/watch?v=VIDEO_ID_LAINNYA
```

**Catatan:** Hapus tanda `#` di depan URL untuk mengaktifkannya!

---

## 📁 Hasil Download

File MP3 akan tersimpan di folder:

```
downloads/
```

Nama file otomatis sesuai judul video YouTube.

---

## ⚡ Troubleshooting Cepat

### Error: "No module named 'colorama'"

**Solusi:**

```bash
venv/Scripts/activate
pip install -r requirements.txt
```

### Error: "FFmpeg not found"

**Solusi:**

```bash
# Restart terminal/PowerShell Anda
# FFmpeg sudah terinstall, hanya perlu refresh PATH
```

Atau install manual dari: https://www.gyan.dev/ffmpeg/builds/

### File tidak muncul di downloads/

**Solusi:**

- Cek apakah ada error di console
- Pastikan URL valid dan video bukan private
- Cek koneksi internet

---

## 🎯 Tips Penggunaan

### Download Playlist

1. Buka playlist YouTube
2. Copy URL setiap video
3. Paste ke `youtube_urls.txt` (satu per baris)
4. Jalankan aplikasi

### Ubah Kualitas Audio

Edit `downloader.py` line 30:

```python
'preferredquality': '320',  # 320kbps (maksimal)
# Ubah ke '192' atau '128' untuk ukuran lebih kecil
```

### Custom Folder Output

Saat aplikasi bertanya "Folder output", ketik nama folder yang diinginkan:

```
Folder output [downloads]: musik-favorit
```

---

## 🔄 Workflow Normal

```
1. Edit youtube_urls.txt
   ↓
2. venv/Scripts/activate
   ↓
3. python downloader.py
   ↓
4. Tekan ENTER (default settings)
   ↓
5. Ketik 'y' (konfirmasi)
   ↓
6. Tunggu download selesai
   ↓
7. Cek folder downloads/
```

---

## ✅ Checklist Sebelum Download

- [ ] Virtual environment sudah aktif (`venv/Scripts/activate`)
- [ ] File `youtube_urls.txt` sudah diisi dengan URL
- [ ] URL tidak ada tanda `#` di depannya
- [ ] Koneksi internet stabil
- [ ] Cukup ruang disk (estimasi: 3-5MB per menit audio)

---

## 📊 Statistik Download

Setelah selesai, aplikasi akan menampilkan:

- ✓ Jumlah berhasil
- ✗ Jumlah gagal
- 📁 Lokasi file

Contoh:

```
======================================================================
📊 RINGKASAN DOWNLOAD 📊
======================================================================
✓ Berhasil: 2/2
✗ Gagal: 0/2
📁 Lokasi file: C:\Users\Dev\Desktop\app-downloader-mp3\downloads
======================================================================
```

---

**Selamat menggunakan! 🎵**
