@echo off
echo ========================================
echo  YouTube MP3 Downloader (Quick Start)
echo ========================================
echo.

REM Cek apakah virtual environment ada
if not exist "venv\Scripts\activate.bat" (
    echo [INFO] Virtual environment belum ada, menjalankan setup...
    call setup.bat
    echo.
)

REM Aktifkan virtual environment
call venv\Scripts\activate.bat

REM Jalankan aplikasi langsung tanpa cek FFmpeg
python downloader.py

REM Deaktivkan virtual environment
deactivate

echo.
pause
