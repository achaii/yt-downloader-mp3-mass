#!/usr/bin/env python3
"""
YouTube MP3 Downloader - Batch Download
Download MP3 dari multiple YouTube videos dengan kualitas terbaik
"""

import os
import sys
import shutil
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
        ffmpeg_path = self._find_ffmpeg()
        
        # Konfigurasi yt-dlp untuk kualitas audio terbaik
        self.ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',  # Kualitas maksimal 320kbps
            }],
            'outtmpl': str(self.output_folder / '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            'ignoreerrors': True,  # Lanjutkan meskipun ada error
            'nocheckcertificate': True,
            'prefer_ffmpeg': True,
        }
        
        # Tambahkan FFmpeg location jika ditemukan
        if ffmpeg_path:
            self.ydl_opts['ffmpeg_location'] = ffmpeg_path
            print(f"{Fore.GREEN}✓ FFmpeg ditemukan: {ffmpeg_path}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠ FFmpeg tidak ditemukan di PATH{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}  File akan didownload dalam format asli (mungkin bukan MP3){Style.RESET_ALL}")
    
    def _find_ffmpeg(self) -> Optional[str]:
        """
        Cari FFmpeg di sistem
        
        Returns:
            Path ke FFmpeg atau None jika tidak ditemukan
        """
        # Cek apakah FFmpeg ada di PATH
        ffmpeg_cmd = shutil.which('ffmpeg')
        if ffmpeg_cmd:
            return str(Path(ffmpeg_cmd).parent)
        
        # Cek lokasi umum di Windows
        common_paths = [
            Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft' / 'WinGet' / 'Packages',
            Path('C:/ffmpeg/bin'),
            Path('C:/Program Files/ffmpeg/bin'),
            Path('C:/Program Files (x86)/ffmpeg/bin'),
        ]
        
        for base_path in common_paths:
            if base_path.exists():
                # Cari di subdirektori untuk instalasi winget
                if 'WinGet' in str(base_path):
                    for subdir in base_path.glob('*ffmpeg*'):
                        # Cari ffmpeg.exe secara rekursif
                        for ffmpeg_exe in subdir.rglob('ffmpeg.exe'):
                            if ffmpeg_exe.exists():
                                return str(ffmpeg_exe.parent)
                else:
                    ffmpeg_exe = base_path / 'ffmpeg.exe'
                    if ffmpeg_exe.exists():
                        return str(base_path)
        
        return None
    
    def read_urls_from_file(self, file_path: str) -> List[str]:
        """
        Membaca URL dari file .txt
        
        Args:
            file_path: Path ke file .txt yang berisi URL
            
        Returns:
            List URL yang valid
        """
        urls = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip baris kosong dan komentar
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
        """
        Download single video sebagai MP3
        
        Args:
            url: URL YouTube video
            index: Index video saat ini
            total: Total video yang akan didownload
            
        Returns:
            True jika berhasil, False jika gagal
        """
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[{index}/{total}] Memproses: {url}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([url])
            
            print(f"\n{Fore.GREEN}✓ Berhasil mendownload [{index}/{total}]{Style.RESET_ALL}\n")
            return True
        
        except Exception as e:
            print(f"\n{Fore.RED}✗ Gagal mendownload [{index}/{total}]: {e}{Style.RESET_ALL}\n")
            return False
    
    def download_batch(self, urls: List[str]) -> dict:
        """
        Download multiple videos sebagai MP3
        
        Args:
            urls: List URL YouTube videos
            
        Returns:
            Dictionary dengan statistik download
        """
        if not urls:
            print(f"{Fore.RED}✗ Tidak ada URL untuk didownload{Style.RESET_ALL}")
            return {'success': 0, 'failed': 0, 'total': 0}
        
        total = len(urls)
        success_count = 0
        failed_count = 0
        
        print(f"\n{Fore.MAGENTA}{'='*70}")
        print(f"🎵 YOUTUBE MP3 DOWNLOADER - BATCH MODE 🎵")
        print(f"{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Total video: {total}")
        print(f"Output folder: {self.output_folder.absolute()}")
        print(f"Kualitas: 320kbps (Maksimal){Style.RESET_ALL}\n")
        
        for index, url in enumerate(urls, 1):
            if self.download_single(url, index, total):
                success_count += 1
            else:
                failed_count += 1
        
        # Tampilkan ringkasan
        print(f"\n{Fore.MAGENTA}{'='*70}")
        print(f"📊 RINGKASAN DOWNLOAD 📊")
        print(f"{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ Berhasil: {success_count}/{total}{Style.RESET_ALL}")
        print(f"{Fore.RED}✗ Gagal: {failed_count}/{total}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📁 Lokasi file: {self.output_folder.absolute()}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'='*70}{Style.RESET_ALL}\n")
        
        return {
            'success': success_count,
            'failed': failed_count,
            'total': total
        }


def main():
    """Main function"""
    print(f"{Fore.MAGENTA}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║         🎵 YOUTUBE MP3 DOWNLOADER - KUALITAS TERBAIK 🎵          ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}\n")
    
    # Default values
    default_url_file = "youtube_urls.txt"
    default_output_folder = "downloads"
    
    # Tanya user untuk custom settings atau gunakan default
    print(f"{Fore.CYAN}Tekan ENTER untuk menggunakan nilai default{Style.RESET_ALL}\n")
    
    url_file = input(f"File URL (.txt) [{default_url_file}]: ").strip() or default_url_file
    output_folder = input(f"Folder output [{default_output_folder}]: ").strip() or default_output_folder
    
    # Validasi file exists
    if not os.path.exists(url_file):
        print(f"\n{Fore.RED}✗ File '{url_file}' tidak ditemukan!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Buat file '{url_file}' dan masukkan URL YouTube (satu per baris){Style.RESET_ALL}")
        sys.exit(1)
    
    # Initialize downloader
    downloader = YouTubeMp3Downloader(output_folder)
    
    # Baca URLs dari file
    urls = downloader.read_urls_from_file(url_file)
    
    if not urls:
        print(f"\n{Fore.YELLOW}⚠ Tidak ada URL valid di file '{url_file}'{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Pastikan setiap baris berisi URL YouTube yang valid{Style.RESET_ALL}")
        sys.exit(1)
    
    # Konfirmasi sebelum download
    print(f"\n{Fore.YELLOW}Akan mendownload {len(urls)} video sebagai MP3 (320kbps)")
    confirm = input(f"Lanjutkan? (y/n): {Style.RESET_ALL}").strip().lower()
    
    if confirm != 'y':
        print(f"{Fore.RED}Download dibatalkan{Style.RESET_ALL}")
        sys.exit(0)
    
    # Mulai batch download
    stats = downloader.download_batch(urls)
    
    # Exit code berdasarkan hasil
    if stats['failed'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}✗ Download dibatalkan oleh user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
        sys.exit(1)
