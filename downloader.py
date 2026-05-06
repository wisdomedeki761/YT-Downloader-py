"""
YouTube Downloader - Download Logic
Handles video/playlist downloads with beautiful progress visualization.
"""

import os
import sys
import threading
import queue
from datetime import datetime
from typing import Optional

import yt_dlp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DownloadProgressHook:
    """Custom progress hook for beautiful terminal progress display."""

    def __init__(self):
        self.downloaded_bytes = 0
        self.total_bytes = 0
        self.speed = 0
        self.eta = 0
        self.filename = ""
        self.last_percentage = -1
        self.start_time = datetime.now()

    def __call__(self, d):
        """Handle download progress updates."""
        if d['status'] == 'downloading':
            self.downloaded_bytes = d.get('downloaded_bytes', 0)
            self.total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            self.speed = d.get('speed', 0)
            self.eta = d.get('eta', 0)
            self.filename = d.get('filename', '')

            # Extract just the filename without path
            if self.filename:
                self.filename = os.path.splitext(os.path.basename(self.filename))[0][:30]

            # Calculate percentage
            if self.total_bytes > 0:
                percentage = (self.downloaded_bytes / self.total_bytes) * 100
            else:
                percentage = 0

            # Only update display if percentage changed by at least 0.5%
            if abs(percentage - self.last_percentage) >= 0.5:
                self.last_percentage = percentage
                self._display_progress()

        elif d['status'] == 'finished':
            self._display_completed()

    def _format_speed(self, bytes_per_sec: float) -> str:
        """Format speed to human readable format."""
        if bytes_per_sec is None:
            return "0 B/s"
        for unit in ['B/s', 'KB/s', 'MB/s', 'GB/s']:
            if bytes_per_sec < 1024:
                return f"{bytes_per_sec:.1f} {unit}"
            bytes_per_sec /= 1024
        return f"{bytes_per_sec:.1f} TB/s"

    def _format_size(self, bytes_size: float) -> str:
        """Format size to human readable format."""
        if bytes_size is None:
            return "0 B"
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024
        return f"{bytes_size:.1f} TB"

    def _format_time(self, seconds: Optional[int]) -> str:
        """Format seconds to time string."""
        if seconds is None:
            return "--:--"
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        if hours > 0:
            return f"{hours}:{mins:02d}:{secs:02d}"
        return f"{mins:02d}:{secs:02d}"

    def _get_progress_bar(self, percentage: float, width: int = 30) -> str:
        """Create a beautiful progress bar."""
        filled = int(width * percentage / 100)
        empty = width - filled
        bar = "█" * filled + "░" * empty
        return f"[{bar}]"

    def _display_progress(self):
        """Display the progress bar in terminal."""
        if self.total_bytes > 0:
            percentage = (self.downloaded_bytes / self.total_bytes) * 100
        else:
            percentage = 0

        # Truncate filename if too long
        display_name = self.filename[:25] + "..." if len(self.filename) > 25 else self.filename

        # Create single-line progress output
        bar = self._get_progress_bar(percentage)
        downloaded = self._format_size(self.downloaded_bytes)
        total = self._format_size(self.total_bytes)
        speed = self._format_speed(self.speed)
        eta = self._format_time(self.eta)

        # Single line progress
        progress_line = f"  {display_name:<28} {bar} {percentage:5.1f}%  {downloaded:>8} / {total:<8}  {speed:<10}  ETA: {eta}"

        # Clear line and print updated progress
        sys.stdout.write("\r" + " " * 100 + "\r" + progress_line)
        sys.stdout.flush()

    def _display_completed(self):
        """Display completion message."""
        sys.stdout.write("\r" + " " * 100 + "\r")
        sys.stdout.flush()
        print(f"  ✓ Download completed!")
        print()


class YouTubeDownloader:
    """Main downloader class."""

    def __init__(self):
        self.download_path = os.getenv('DOWNLOAD_PATH', './downloads')
        self.progress_hook = DownloadProgressHook()

    def _get_quality_format(self, quality_choice: str) -> dict:
        """Get yt-dlp format based on quality selection."""
        quality_map = {
            '1': {'format': 'bestvideo[height<=360]+bestaudio/best', 'ext': '360p'},
            '2': {'format': 'bestvideo[height<=720]+bestaudio/best', 'ext': '720p'},
            '3': {'format': 'bestvideo[height<=1080]+bestaudio/best', 'ext': '1080p'},
            '4': {'format': 'best', 'ext': 'best'},
        }
        return quality_map.get(quality_choice, quality_map['4'])

    def _get_audio_format(self) -> dict:
        """Get audio-only format."""
        return {'format': 'bestaudio/best', 'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]}

    def download_single_video(self, url: str, quality: str, audio_only: bool = False):
        """Download a single YouTube video."""
        print(f"\n📥 Downloading single video...")
        print(f"   URL: {url}\n")

        # Ensure download directory exists
        os.makedirs(self.download_path, exist_ok=True)

        # Get FFmpeg path
        ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg-8.1-essentials_build', 'bin', 'ffmpeg.exe')

        if audio_only:
            ydl_opts = self._get_audio_format()
            ydl_opts['ffmpeg_location'] = ffmpeg_path
        else:
            format_info = self._get_quality_format(quality)
            ydl_opts = {
                'format': format_info['format'],
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'quiet': True,
                'no_warnings': True,
                'ffmpeg_location': ffmpeg_path,
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=True)
                print(f"\n✅ Successfully downloaded: {info['title']}")
            except Exception as e:
                print(f"\n❌ Error: {e}")

    def download_playlist(self, url: str, quality: str, audio_only: bool = False, concurrent: int = 1):
        """Download an entire YouTube playlist using flat-playlist method."""
        print(f"\n📥 Downloading playlist...")
        print(f"   URL: {url}\n")

        # Get FFmpeg path
        ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg-8.1-essentials_build', 'bin', 'ffmpeg.exe')

        # Step 1: Get playlist name
        print("   🔍 Fetching playlist info...")
        try:
            import subprocess
            result = subprocess.run(
                ['yt-dlp', '--flat-playlist', '--print', 'playlist_title', url],
                capture_output=True,
                text=True,
                timeout=30
            )
            playlist_name = result.stdout.strip()
            if not playlist_name:
                playlist_name = "Playlist"
            # Sanitize folder name
            playlist_folder = "".join(c for c in playlist_name if c.isalnum() or c in (' ', '-', '_')).strip()
            playlist_folder = playlist_folder[:50]
        except Exception:
            playlist_folder = "Playlist"

        # Step 2: Extract all video URLs using --flat-playlist
        print("   📡 Extracting video URLs...")
        try:
            result = subprocess.run(
                ['yt-dlp', '--flat-playlist', '--print', 'url', url],
                capture_output=True,
                text=True,
                timeout=60
            )
            video_urls = result.stdout.strip().split('\n')
            video_urls = [v for v in video_urls if v.strip() and v.strip().startswith('http')]
            total_videos = len(video_urls)
            mode_str = "parallel" if concurrent > 1 else "sequential"
            print(f"   ✅ Found: '{playlist_folder}' ({total_videos} videos) [{mode_str} mode]\n")
        except Exception as e:
            print(f"   ❌ Error extracting playlist: {e}")
            return

        if not video_urls:
            print("   ❌ No videos found in playlist!")
            return

        # Step 3: Create playlist folder
        playlist_path = os.path.join(self.download_path, playlist_folder)
        os.makedirs(playlist_path, exist_ok=True)
        print(f"   📁 Folder: {playlist_path}\n")

        # Step 4: Download videos
        downloaded = 0
        failed = 0
        lock = threading.Lock()

        def download_worker(video_url: str, worker_id: int):
            """Worker function for parallel downloads."""
            nonlocal downloaded, failed

            if audio_only:
                ydl_opts = self._get_audio_format()
                ydl_opts['ffmpeg_location'] = ffmpeg_path
                ydl_opts['outtmpl'] = os.path.join(playlist_path, '%(title)s.%(ext)s')
                ydl_opts['progress_hooks'] = [self.progress_hook]
                ydl_opts['quiet'] = True
                ydl_opts['no_warnings'] = True
            else:
                format_info = self._get_quality_format(quality)
                ydl_opts = {
                    'format': format_info['format'],
                    'outtmpl': os.path.join(playlist_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [self.progress_hook],
                    'quiet': True,
                    'no_warnings': True,
                    'ffmpeg_location': ffmpeg_path,
                }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                with lock:
                    downloaded += 1
            except Exception:
                with lock:
                    failed += 1

        if concurrent <= 1:
            # Sequential download
            for i, video_url in enumerate(video_urls, 1):
                print(f"   [{i}/{total_videos}] Downloading...", end='\r')
                sys.stdout.flush()
                download_worker(video_url, 1)
        else:
            # Parallel download using threads
            print(f"   🚀 Starting {concurrent} concurrent downloads...\n")
            video_queue = queue.Queue()
            for url in video_urls:
                video_queue.put(url)

            def worker():
                while not video_queue.empty():
                    video_url = video_queue.get()
                    download_worker(video_url, 1)
                    video_queue.task_done()

            threads = []
            for _ in range(concurrent):
                t = threading.Thread(target=worker)
                t.daemon = True
                t.start()
                threads.append(t)

            # Wait for all downloads to complete
            video_queue.join()

            # Show final progress
            print(f"\n   [{downloaded + failed}/{total_videos}] All downloads complete!")

        # Summary
        print(f"\n\n   ✅ Downloaded: {downloaded}")
        print(f"   ❌ Failed: {failed}")
        print(f"   📊 Total: {total_videos}")