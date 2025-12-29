@echo off
setlocal
title Setup YouTube Downloader Environment

echo ==================================================
echo      YouTube MP3 Downloader - Setup Environment
echo ==================================================
echo.

cd /d "%~dp0"

REM 1. Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install properly.
    pause
    exit /b 1
)
echo [OK] Python found.

REM 2. Create Virtual Environment
set "VENV_DIR=venv"

if not exist "%VENV_DIR%" (
    echo [INFO] Creating virtual environment...
    python -m venv "%VENV_DIR%" >nul 2>&1
    if not exist "%VENV_DIR%\Scripts\python.exe" (
        echo [WARNING] Native venv failed. Using virtualenv.pyz...
        curl -sSL https://bootstrap.pypa.io/virtualenv.pyz -o virtualenv.pyz
        python virtualenv.pyz "%VENV_DIR%"
        del virtualenv.pyz
    )
    echo [OK] Virtual environment created.
)

REM 3. Install Dependencies
echo.
echo [INFO] Installing dependencies...
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo [ERROR] Python VENV not found.
    pause
    exit /b 1
)
"%VENV_DIR%\Scripts\python.exe" -m pip install --upgrade pip
if exist "requirements.txt" (
    "%VENV_DIR%\Scripts\pip.exe" install --upgrade -r requirements.txt
)

REM 4. Auto-Install Portable FFmpeg (No-Hassle)
echo.
echo [INFO] Checking FFmpeg...

REM Check PATH
ffmpeg -version >nul 2>&1
if not errorlevel 1 (
    echo [OK] FFmpeg found in PATH.
    goto :finish
)

REM Check Local bin
if exist "bin\ffmpeg.exe" (
    echo [OK] FFmpeg found in local 'bin' folder.
    goto :finish
)

echo [WARNING] FFmpeg not found on system.
echo [INFO] Downloading Portable FFmpeg (Auto-Install)...
echo        This may take a minute...

if not exist "bin" mkdir "bin"

REM Download Zip
curl -L -o ffmpeg.zip https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip

if not exist "ffmpeg.zip" (
    echo [ERROR] Download failed. Check internet.
    pause
    exit /b 1
)

echo [INFO] Extracting FFmpeg...
powershell -Command "Expand-Archive -Path ffmpeg.zip -DestinationPath bin_tmp -Force"

echo [INFO] Setting up binaries...
REM Move exe files to bin root
for /r "bin_tmp" %%f in (ffmpeg.exe ffprobe.exe) do move /y "%%f" "bin\" >nul

REM Cleanup
del ffmpeg.zip
rmdir /s /q "bin_tmp"

if exist "bin\ffmpeg.exe" (
    echo [SUCCESS] Portable FFmpeg installed to 'bin/' folder!
) else (
    echo [ERROR] Failed to set up FFmpeg.
)

:finish
REM 5. Workspace Check
if not exist "downloads" mkdir downloads
if not exist "youtube_urls.txt" echo # URL here > youtube_urls.txt

echo.
echo ==================================================
echo      Setup Complete! Run 'download.bat'
echo ==================================================
pause
