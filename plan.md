# YouTube Downloader CLI Project Plan

## Project Goal

Build a terminal-based Python application that can:

-   Download a single YouTube video
-   Download an entire YouTube playlist
-   Let user select download quality (360p, 720p, 1080p, best)
-   Let user choose audio-only or video download
-   Let user specify custom download folder via .env file
-   Create organized folder structure for downloads
-   Show download progress
-   Support best video quality download

------------------------------------------------------------------------

## Tech Stack

-   Python 3.14+
-   yt-dlp
-   python-dotenv
-   FFmpeg (included in project)

------------------------------------------------------------------------

## Project Structure

``` bash
youtube-downloader/
│
├── main.py
├── downloader.py
├── .env
├── requirements.txt
├── README.md
└── ffmpeg-8.1-essentials_build/  # FFmpeg included
```

------------------------------------------------------------------------

## Setup Instructions

### 1. Create virtual environment

``` bash
python -m venv venv
```

Activate:

**Windows**

``` bash
venv\Scripts\activate
```

**Linux/Mac**

``` bash
source venv/bin/activate
```

------------------------------------------------------------------------

### 2. Install dependencies

``` bash
pip install yt-dlp python-dotenv
```

------------------------------------------------------------------------

## Configuration (.env)

Create a `.env` file in the project root:

``` env
DOWNLOAD_PATH=D:\YT Dowanload
```

------------------------------------------------------------------------

## User Flow

When starting the application, the user sees:

```
=== YouTube Downloader ===
1. Download a single YouTube video
2. Download an entire YouTube playlist
3. Exit

Enter your choice (1-3):
```

After selecting an option:

```
Enter YouTube URL: https://youtube.com/watch?v=...

Select quality:
1. 360p
2. 720p
3. 1080p
4. Best available

Enter your choice (1-4):

Download type:
1. Video + Audio
2. Audio only

Enter your choice (1-2):
```

Download starts and creates:
- For single video: `D:\YT Dowanload\VideoTitle.ext`
- For playlist: `D:\YT Dowanload\PlaylistName\VideoTitle.ext`

------------------------------------------------------------------------

## Features To Implement

### Phase 1 (MVP)

-   Show main menu with 2 download options
-   Accept YouTube URL from terminal
-   Ask for quality selection
-   Ask for audio-only or video
-   Download video(s) to .env configured path
-   Create folder for playlist downloads
-   Progress percentage

### Phase 2

-   Error handling
-   Retry failed downloads
-   Subtitle download

------------------------------------------------------------------------

## Core Logic

### main.py

Responsibilities:
-   Display main menu
-   Get user choice (single video / playlist)
-   Get URL input
-   Get quality preference
-   Get download type (video/audio)
-   Call downloader with appropriate parameters

### downloader.py

Responsibilities:
-   Configure yt-dlp with quality settings
-   Create output folder structure
-   Handle single video download
-   Handle playlist download (create playlist folder)
-   Show progress callback
-   Handle errors and retries
(video/audio) - Call downloader module

### downloader.py

Responsibilities: - Configure yt-dlp options - Handle playlist
download - Handle single video download - Display progress hooks

Example options:

``` python
{
    "format": "best",
    "outtmpl": f"{path}/%(title)s.%(ext)s"
}
```

------------------------------------------------------------------------

## Commands To Run

``` bash
python main.py
```

Expected flow:

1.  Enter YouTube URL
2.  Enter output path
3.  Download starts

------------------------------------------------------------------------

## Future Improvements

-   Package into executable with PyInstaller
-   GUI version using Tkinter or CustomTkinter
-   Download history log
-   Resume interrupted downloads

------------------------------------------------------------------------

## Success Criteria

Project is complete when: - User can paste any YouTube video URL and
download successfully - User can paste playlist URL and download full
playlist - Files save correctly in chosen folder
