# 🎬 YouTube Downloader CLI

A beautiful terminal-based YouTube video and playlist downloader with an interactive menu, quality selection, and progress visualization.

![YouTube Downloader](https://img.shields.io/badge/Python-3.14+-blue?style=for-the-badge&logo=python)
![yt-dlp](https://img.shields.io/badge/yt--dlp-2024-yellow?style=for-the-badge)

---

## ✨ Features

- 🚀 **Interactive CLI Menu** - Easy to use terminal interface
- 📺 **Single Video & Playlist Support** - Download one video or entire playlists
- 🎨 **Quality Selection** - Choose 360p, 720p, 1080p, or best available
- 🎵 **Audio Only Mode** - Extract audio from videos
- 📊 **Beautiful Progress Bar** - Visual download progress with percentage
- 📁 **Organized Downloads** - Automatic folder creation for playlists
- ⚡ **Concurrent Downloads** - Download multiple playlist videos in parallel (1-10 at once)
- ⚡ **Fast & Reliable** - Powered by yt-dlp

---

## 📋 Requirements

- Python 3.14 or higher
- Windows, Linux, or macOS

---

## 🚀 Quick Start

### 1. Clone or navigate to the project

```bash
cd youtube-downloader
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure download path

Edit `.env` file and set your download folder:

```env
DOWNLOAD_PATH=D:\YT Download
```

### 6. Run the application

```bash
.\venv\Scripts\activate
python main.py
```

---

## 📖 Usage

1. **Start the application:**
   ```bash
   .\venv\Scripts\activate ; python main.py
   ```

2. **Choose download type:**
   ```
   === YouTube Downloader ===
   1. Download a single YouTube video
   2. Download an entire YouTube playlist
   3. Exit

   Enter your choice (1-3): _
   ```

3. **Enter YouTube URL:**
   ```
   Enter YouTube URL: https://youtube.com/watch?v=...
   ```

4. **Select quality:**
   ```
   Select quality:
   1. 360p
   2. 720p
   3. 1080p
   4. Best available

   Enter your choice (1-4): _
   ```

5. **Choose download type:**
   ```
   Download type:
   1. Video + Audio
   2. Audio only

   Enter your choice (1-2): _
   ```

6. **Concurrent downloads (playlist only):**
   ```
   Concurrent downloads:
   1. No (one at a time)
   2. Yes (parallel)

   Enable parallel downloads? (1-2): 2
   How many concurrent downloads? (1-10): 5
   ```

7. **Watch the progress!**
   ```
   Downloading: Video Title
   ████████████████████░░░░ 75%
   ```

---

## 📁 Project Structure

```
youtube-downloader/
├── main.py                      # Main application entry point
├── downloader.py                # Download logic with progress bar
├── requirements.txt             # Python dependencies
├── .env                         # Configuration (download path)
├── README.md                    # This file
├── ffmpeg-8.1-essentials_build/ # FFmpeg for video processing
└── venv/                        # Virtual environment
```

---

## ⚙️ Configuration

### .env File

Create or edit `.env` to set your download location:

```env
# Windows example
DOWNLOAD_PATH=D:\YT Download

# Linux/Mac example
DOWNLOAD_PATH=/home/user/Downloads/YT
```

---

## 🎨 Progress Bar Preview

```
Downloading: Amazing Video Title
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ████████████████████░░░░  75%  75.5 MB / 100.0 MB
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.14+ | Core language |
| yt-dlp | YouTube downloading |
| python-dotenv | Configuration management |
| FFmpeg | Video/audio processing |

---

## 📝 Notes

- FFmpeg is included in the project for Windows
- On Linux/Mac, install FFmpeg separately: `sudo apt install ffmpeg`
- Multiple instances can run simultaneously in different terminals
- Playlist downloads automatically create a folder with the playlist name

---

## 📄 License

MIT License - Feel free to use and modify!

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

**Made with ❤️ for YouTube enthusiasts**