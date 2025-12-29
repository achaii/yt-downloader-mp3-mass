@echo off
title YouTube Downloader
if not exist "venv" (
    echo [ERROR] Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python downloader.py
pause
