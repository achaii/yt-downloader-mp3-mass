@echo off
echo ========================================
echo  YouTube MP3 Downloader - Setup
echo ========================================
echo.

REM Cek apakah Python terinstall
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan!
    echo Silakan install Python dari https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Membuat virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Gagal membuat virtual environment!
    pause
    exit /b 1
)

echo [2/3] Mengaktifkan virtual environment...
call venv\Scripts\activate.bat

echo [3/3] Menginstall dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Gagal menginstall dependencies!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Setup Selesai!
echo ========================================
echo.
echo PENTING: Install FFmpeg terlebih dahulu!
echo.
echo Cara install FFmpeg:
echo 1. Download dari: https://www.gyan.dev/ffmpeg/builds/
echo 2. Extract ke folder (misal: C:\ffmpeg)
echo 3. Tambahkan ke PATH: C:\ffmpeg\bin
echo.
echo Atau gunakan command (Run as Administrator):
echo   winget install ffmpeg
echo.
echo Setelah FFmpeg terinstall, jalankan:
echo   run.bat
echo.
pause
