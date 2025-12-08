#!/usr/bin/env python3
"""
Converter - Convert audio files to MP3
Mengkonversi semua file audio di folder downloads ke MP3 320kbps
"""

import os
import sys
import shutil
from pathlib import Path
from colorama import Fore, Style, init
import subprocess

# Initialize colorama
init(autoreset=True)

def find_ffmpeg():
    """Cari FFmpeg di sistem"""
    # Cek di PATH
    ffmpeg_cmd = shutil.which('ffmpeg')
    if ffmpeg_cmd:
        return ffmpeg_cmd
    
    # Cek lokasi umum di Windows
    common_paths = [
        Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft' / 'WinGet' / 'Packages',
        Path('C:/ffmpeg/bin'),
        Path('C:/Program Files/ffmpeg/bin'),
        Path('C:/Program Files (x86)/ffmpeg/bin'),
    ]
    
    for base_path in common_paths:
        if base_path.exists():
            if 'WinGet' in str(base_path):
                # Cari di semua subdirektori ffmpeg
                for subdir in base_path.glob('*ffmpeg*'):
                    # Cari ffmpeg.exe secara rekursif
                    for ffmpeg_exe in subdir.rglob('ffmpeg.exe'):
                        if ffmpeg_exe.exists():
                            return str(ffmpeg_exe)
            else:
                ffmpeg_exe = base_path / 'ffmpeg.exe'
                if ffmpeg_exe.exists():
                    return str(ffmpeg_exe)
    
    return None

def convert_to_mp3(input_file, output_file, ffmpeg_path):
    """Convert file audio ke MP3 320kbps"""
    try:
        cmd = [
            ffmpeg_path,
            '-i', str(input_file),
            '-vn',  # No video
            '-ar', '44100',  # Sample rate
            '-ac', '2',  # Stereo
            '-b:a', '320k',  # Bitrate 320kbps
            '-y',  # Overwrite
            str(output_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return False

def main():
    print(f"{Fore.MAGENTA}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║              🎵 AUDIO TO MP3 CONVERTER - 320kbps 🎵              ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}\n")
    
    # Cari FFmpeg
    ffmpeg_path = find_ffmpeg()
    if not ffmpeg_path:
        print(f"{Fore.RED}✗ FFmpeg tidak ditemukan!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Silakan install FFmpeg terlebih dahulu:{Style.RESET_ALL}")
        print(f"  1. Jalankan: install-ffmpeg.bat")
        print(f"  2. Atau download dari: https://www.gyan.dev/ffmpeg/builds/")
        sys.exit(1)
    
    print(f"{Fore.GREEN}✓ FFmpeg ditemukan: {ffmpeg_path}{Style.RESET_ALL}\n")
    
    # Folder downloads
    downloads_folder = Path('downloads')
    if not downloads_folder.exists():
        print(f"{Fore.RED}✗ Folder 'downloads' tidak ditemukan!{Style.RESET_ALL}")
        sys.exit(1)
    
    # Cari semua file audio non-MP3
    audio_extensions = ['.webm', '.m4a', '.opus', '.ogg', '.aac', '.wav', '.flac']
    audio_files = []
    
    for ext in audio_extensions:
        audio_files.extend(downloads_folder.glob(f'*{ext}'))
    
    if not audio_files:
        print(f"{Fore.YELLOW}⚠ Tidak ada file audio untuk dikonversi{Style.RESET_ALL}")
        print(f"{Fore.CYAN}File MP3 sudah ada atau folder kosong{Style.RESET_ALL}")
        sys.exit(0)
    
    print(f"{Fore.CYAN}Ditemukan {len(audio_files)} file untuk dikonversi:{Style.RESET_ALL}")
    for f in audio_files:
        print(f"  - {f.name}")
    
    print(f"\n{Fore.YELLOW}Konversi ke MP3 320kbps?{Style.RESET_ALL}")
    confirm = input("Lanjutkan? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print(f"{Fore.RED}Konversi dibatalkan{Style.RESET_ALL}")
        sys.exit(0)
    
    # Konversi setiap file
    print(f"\n{Fore.MAGENTA}{'='*70}{Style.RESET_ALL}")
    success_count = 0
    failed_count = 0
    
    for i, audio_file in enumerate(audio_files, 1):
        output_file = audio_file.with_suffix('.mp3')
        
        print(f"\n{Fore.CYAN}[{i}/{len(audio_files)}] {audio_file.name}{Style.RESET_ALL}")
        print(f"  → {output_file.name}")
        
        if convert_to_mp3(audio_file, output_file, ffmpeg_path):
            print(f"  {Fore.GREEN}✓ Berhasil{Style.RESET_ALL}")
            
            # Hapus file asli setelah konversi berhasil
            try:
                audio_file.unlink()
                print(f"  {Fore.GREEN}✓ File asli dihapus{Style.RESET_ALL}")
            except Exception as e:
                print(f"  {Fore.YELLOW}⚠ Gagal menghapus file asli: {e}{Style.RESET_ALL}")
            
            success_count += 1
        else:
            print(f"  {Fore.RED}✗ Gagal{Style.RESET_ALL}")
            failed_count += 1
    
    # Ringkasan
    print(f"\n{Fore.MAGENTA}{'='*70}")
    print(f"📊 RINGKASAN KONVERSI 📊")
    print(f"{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ Berhasil: {success_count}/{len(audio_files)}{Style.RESET_ALL}")
    print(f"{Fore.RED}✗ Gagal: {failed_count}/{len(audio_files)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📁 Lokasi: {downloads_folder.absolute()}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'='*70}{Style.RESET_ALL}\n")
    
    if failed_count > 0:
        sys.exit(1)
    else:
        print(f"{Fore.GREEN}🎉 Semua file berhasil dikonversi ke MP3!{Style.RESET_ALL}\n")
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}✗ Konversi dibatalkan oleh user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
        sys.exit(1)
