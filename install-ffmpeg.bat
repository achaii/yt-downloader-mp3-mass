@echo off
echo ========================================
echo  FFmpeg Installer
echo ========================================
echo.

REM Cek apakah FFmpeg sudah terinstall
ffmpeg -version >nul 2>&1
if not errorlevel 1 (
    echo FFmpeg sudah terinstall!
    ffmpeg -version
    echo.
    pause
    exit /b 0
)

echo Mencoba install FFmpeg menggunakan winget...
echo.

REM Coba install dengan winget
winget install --id=Gyan.FFmpeg -e
if not errorlevel 1 (
    echo.
    echo ========================================
    echo  FFmpeg berhasil diinstall!
    echo ========================================
    echo.
    echo PENTING: Restart terminal/command prompt Anda
    echo agar FFmpeg dapat digunakan.
    echo.
    pause
    exit /b 0
)

echo.
echo [INFO] winget tidak tersedia atau gagal.
echo.
echo Silakan install FFmpeg secara manual:
echo.
echo 1. Download dari: https://www.gyan.dev/ffmpeg/builds/
echo    Pilih: ffmpeg-release-essentials.zip
echo.
echo 2. Extract ke folder (misal: C:\ffmpeg)
echo.
echo 3. Tambahkan ke PATH:
echo    - Buka System Properties ^> Environment Variables
echo    - Edit PATH, tambahkan: C:\ffmpeg\bin
echo    - Klik OK dan restart terminal
echo.
echo 4. Verifikasi dengan command: ffmpeg -version
echo.
pause
