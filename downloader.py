#!/usr/bin/env python3
"""
YouTube MP3 Downloader & Converter
Download MP3 dari YouTube atau convert file lokal
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional
import yt_dlp
from colorama import Fore, Style, init

# Initialize colorama untuk Windows
init(autoreset=True)

class YouTubeMp3Downloader:
    def __init__(self, output_folder: str = "downloads"):
        """
        Initialize downloader dengan folder output
        
        Args:
            output_folder: Folder untuk menyimpan file MP3
        """
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)
        
        # Cari FFmpeg
        self.ffmpeg_path = self._find_ffmpeg()
        
        # Konfigurasi yt-dlp untuk kualitas audio terbaik
        self.ydl_opts = {
            'format': 'bestaudio/best',  # Ambil audio terbaik format apa saja
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',  # 192kbps adalah standarnya, 320 bisa bloated
            }],
            'outtmpl': str(self.output_folder / '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            'ignoreerrors': True,
            'nocheckcertificate': True,
            'prefer_ffmpeg': True,
            'keepvideo': False,  # Pastikan file asli dihapus
            # Anti-Bot Options
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
            'sleep_interval': 3,
            'max_sleep_interval': 10,
        }

        # Cek cookies.txt
        if os.path.exists("cookies.txt"):
            self.ydl_opts['cookiefile'] = "cookies.txt"
            print(f"{Fore.GREEN}✓ Menggunakan cookies.txt{Style.RESET_ALL}")
        
        # Tambahkan FFmpeg location jika ditemukan
        if self.ffmpeg_path:
            self.ydl_opts['ffmpeg_location'] = self.ffmpeg_path
            print(f"{Fore.GREEN}✓ FFmpeg ditemukan: {self.ffmpeg_path}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠ FFmpeg tidak ditemukan di PATH{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}  File akan didownload dalam format asli (mungkin bukan MP3){Style.RESET_ALL}")
    
    def _find_ffmpeg(self) -> Optional[str]:
        """Cari FFmpeg di sistem"""
        # 1. Cek PATH env var
        if shutil.which('ffmpeg'):
            return str(Path(shutil.which('ffmpeg')).parent)
        
        # 2. Cek lokasi manual umum (Prioritaskan local bin)
        common_paths = [
            Path(__file__).parent / 'bin',  # Local bin folder
            Path('C:/ffmpeg/bin'),
            Path(os.environ.get('ProgramFiles', 'C:/Program Files')) / 'ffmpeg/bin',
            Path(os.environ.get('ProgramFiles(x86)', 'C:/Program Files (x86)')) / 'ffmpeg/bin',
            Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft' / 'WinGet' / 'Packages',
            Path(os.environ.get('ChocolateyInstall', '')) / 'bin',
        ]
        
        for base_path in common_paths:
            if not base_path.exists(): continue
            
            # Direct check
            if (base_path / 'ffmpeg.exe').exists():
                return str(base_path)
                
            # Recursive check (slow but thorough)
            for file in base_path.rglob('ffmpeg.exe'):
                return str(file.parent)
        
        return None
    
    def read_urls_from_file(self, file_path: str) -> List[str]:
        """Membaca URL dari file .txt"""
        urls = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        urls.append(line)
            
            print(f"{Fore.GREEN}✓ Berhasil membaca {len(urls)} URL dari {file_path}{Style.RESET_ALL}")
            return urls
        except FileNotFoundError:
            print(f"{Fore.RED}✗ File tidak ditemukan: {file_path}{Style.RESET_ALL}")
            return []
        except Exception as e:
            print(f"{Fore.RED}✗ Error membaca file: {e}{Style.RESET_ALL}")
            return []
    
    def download_single(self, url: str, index: int, total: int) -> bool:
        """Download single video sebagai MP3"""
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[{index}/{total}] Memproses: {url}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([url])
            
            # Post-Processing Safety Net:
            # Jika yt-dlp gagal convert (sisa file webm/m4a), kita convert manual
            self._ensure_mp3_conversion()

            print(f"\n{Fore.GREEN}✓ Berhasil mendownload [{index}/{total}]{Style.RESET_ALL}\n")
            return True
        
        except Exception as e:
            print(f"\n{Fore.RED}✗ Gagal mendownload [{index}/{total}]: {e}{Style.RESET_ALL}\n")
            return False

    def _ensure_mp3_conversion(self):
        """Cek jika ada file non-MP3 tersisa dan paksa convert ke MP3"""
        audio_extensions = ['.webm', '.m4a', '.opus', '.ogg', '.aac', '.wav', '.flac']
        
        # Tentukan executable ffmpeg
        if self.ffmpeg_path:
            ffmpeg_exe = str(Path(self.ffmpeg_path) / 'ffmpeg.exe')
        elif shutil.which('ffmpeg'):
            ffmpeg_exe = shutil.which('ffmpeg')
        else:
            print(f"{Fore.RED}CRITICAL: FFmpeg tidak ditemukan. Tidak dapat mengkonversi ke MP3.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Tip: Install FFmpeg dan restart terminal.{Style.RESET_ALL}")
            return

        for file_path in self.output_folder.glob("*"):
            if file_path.suffix.lower() in audio_extensions:
                mp3_path = file_path.with_suffix('.mp3')
                
                # Jika MP3 nya belum ada, kita convert
                if not mp3_path.exists():
                    print(f"\n{Fore.YELLOW}⚠ Mengkonversi sisa file ke MP3: {file_path.name}{Style.RESET_ALL}")
                    try:
                        cmd = [
                            ffmpeg_exe, '-i', str(file_path), 
                            '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k', 
                            '-y', str(mp3_path)
                        ]
                        # Use shell=True specifically to help find executable on some Windows envs
                        subprocess.run(cmd, capture_output=True, check=True)
                        print(f"{Fore.GREEN}✓ Konversi Sukses.{Style.RESET_ALL}")
                        
                        # Hapus file asli setelah sukses
                        try:
                            file_path.unlink()
                        except: pass
                    except subprocess.CalledProcessError as e:
                        print(f"{Fore.RED}✗ Gagal konversi (FFmpeg Error): {e}{Style.RESET_ALL}")
                    except FileNotFoundError:
                        print(f"{Fore.RED}✗ Gagal: FFmpeg exe tidak ditemukan di '{ffmpeg_exe}'{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}✗ Gagal konversi: {e}{Style.RESET_ALL}")
                else:
                    try:
                        file_path.unlink()
                    except: pass
    
    def download_batch(self, urls: List[str]):
        """Download multiple videos sebagai MP3"""
        if not urls:
            print(f"{Fore.RED}✗ Tidak ada URL untuk didownload{Style.RESET_ALL}")
            return
        
        total = len(urls)
        success_count = 0
        failed_count = 0
        
        print(f"\n{Fore.MAGENTA}{'='*70}")
        print(f"🎵 BATCH DOWNLOAD MODE 🎵")
        print(f"{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Total video: {total}")
        print(f"Output folder: {self.output_folder.absolute()}{Style.RESET_ALL}\n")
        
        for index, url in enumerate(urls, 1):
            if self.download_single(url, index, total):
                success_count += 1
            else:
                failed_count += 1
        
        self._print_summary(success_count, failed_count, total, "DOWNLOAD")

    def convert_local_files(self):
        """Konversi file lokal non-MP3 ke MP3"""
        print(f"\n{Fore.MAGENTA}{'='*70}")
        print(f"🎵 LOCAL CONVERSION MODE 🎵")
        print(f"{'='*70}{Style.RESET_ALL}")
        
        ffmpeg_exe = 'ffmpeg'
        if self.ffmpeg_path:
            ffmpeg_exe = str(Path(self.ffmpeg_path) / 'ffmpeg.exe')

        # Check ffmpeg availability for subprocess
        try:
            subprocess.run([ffmpeg_exe, '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"{Fore.RED}✗ FFmpeg tidak dapat dijalankan untuk konversi lokal.{Style.RESET_ALL}")
            return

        audio_extensions = ['.webm', '.m4a', '.opus', '.ogg', '.aac', '.wav', '.flac']
        audio_files = []
        for ext in audio_extensions:
            audio_files.extend(self.output_folder.glob(f'*{ext}'))
        
        if not audio_files:
            print(f"{Fore.YELLOW}⚠ Tidak ada file audio non-MP3 ditemukan di {self.output_folder}{Style.RESET_ALL}")
            return

        print(f"{Fore.CYAN}Ditemukan {len(audio_files)} file untuk dikonversi.{Style.RESET_ALL}")
        confirm = input("Lanjutkan konversi? (y/n): ").strip().lower()
        if confirm != 'y': return

        success_count = 0
        failed_count = 0
        total = len(audio_files)

        for i, input_file in enumerate(audio_files, 1):
            output_file = input_file.with_suffix('.mp3')
            print(f"\n{Fore.CYAN}[{i}/{total}] Converting: {input_file.name}{Style.RESET_ALL}")
            
            cmd = [
                ffmpeg_exe, '-i', str(input_file), '-vn', '-ar', '44100', 
                '-ac', '2', '-b:a', '320k', '-y', str(output_file)
            ]
            
            try:
                subprocess.run(cmd, capture_output=True, check=True)
                print(f"{Fore.GREEN}✓ Berhasil{Style.RESET_ALL}")
                try:
                    input_file.unlink()
                    print(f"  File asli dihapus")
                except: pass
                success_count += 1
            except Exception as e:
                print(f"{Fore.RED}✗ Gagal: {e}{Style.RESET_ALL}")
                failed_count += 1
        
        self._print_summary(success_count, failed_count, total, "KONVERSI")

    def _print_summary(self, success, failed, total, label):
        print(f"\n{Fore.MAGENTA}{'='*70}")
        print(f"📊 RINGKASAN {label} 📊")
        print(f"{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ Berhasil: {success}/{total}{Style.RESET_ALL}")
        print(f"{Fore.RED}✗ Gagal: {failed}/{total}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📁 Lokasi: {self.output_folder.absolute()}{Style.RESET_ALL}\n")


def main():
    print(f"{Fore.MAGENTA}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║          🎵 YOUTUBE MP3 DOWNLOADER & CONVERTER 🎵                ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}\n")
    
    downloader = YouTubeMp3Downloader("downloads")
    
    while True:
        print("\nPilih Menu:")
        print("1. Download dari youtube_urls.txt (Default)")
        print("2. Konversi file lokal di folder 'downloads' ke MP3")
        print("3. Keluar")
        
        choice = input("\nPilihan [1]: ").strip() or "1"
        
        if choice == "1":
            url_file = "youtube_urls.txt"
            if not os.path.exists(url_file):
                print(f"{Fore.RED}✗ File {url_file} tidak ditemukan!{Style.RESET_ALL}")
                continue
            urls = downloader.read_urls_from_file(url_file)
            if urls:
                downloader.download_batch(urls)
            break # Exit after download in simple mode, or maybe loop? User request implies run once. Let's break.
        elif choice == "2":
            downloader.convert_local_files()
            break
        elif choice == "3":
            sys.exit(0)
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Dibatalkan.{Style.RESET_ALL}")
