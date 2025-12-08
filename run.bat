@echo off
echo ========================================
echo  YouTube MP3 Downloader
echo ========================================
echo.

REM Cek apakah virtual environment ada
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment tidak ditemukan!
    echo Jalankan setup.bat terlebih dahulu.
    echo.
    pause
    exit /b 1
)

REM Aktifkan virtual environment
call venv\Scripts\activate.bat

REM Cek apakah FFmpeg terinstall
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] FFmpeg tidak ditemukan di PATH!
    echo.
    echo Download FFmpeg dari: https://www.gyan.dev/ffmpeg/builds/
    echo Atau install dengan: winget install ffmpeg
    echo.
    echo Tekan Ctrl+C untuk batal, atau
    pause
)

REM Jalankan aplikasi
python downloader.py

REM Deaktivkan virtual environment
deactivate

echo.
pause
