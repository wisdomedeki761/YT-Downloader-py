"""
YouTube Downloader - Main Application
Interactive CLI menu for downloading YouTube videos and playlists.
"""

import os
import sys
from downloader import YouTubeDownloader


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    """Print the application banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║    ██████╗ ██████╗ ██╗   ██╗██╗  ██╗██╗   ██╗██████╗     ║
    ║   ██╔════╝██╔═══██╗╚██╗ ██╔╝██║  ██║██║   ██║██╔══██╗    ║
    ║   ██║     ██║   ██║ ╚████╔╝ ███████║██║   ██║██████╔╝    ║
    ║   ██║     ██║   ██║  ╚██╔╝  ██╔══██║██║   ██║██╔═══╝     ║
    ║   ╚██████╗╚██████╔╝   ██║   ██║  ██║╚██████╔╝██║         ║
    ║    ╚═════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝         ║
    ║                                                           ║
    ║                    🚀 Qx Dev 🚀                          ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_menu():
    """Print the main menu."""
    menu = """
    ┌─────────────────────────────────────────────────────────┐
    │                    MAIN MENU                            │
    ├─────────────────────────────────────────────────────────┤
    │                                                         │
    │   1. 📺 Download a single YouTube video                 │
    │   2. 📋 Download an entire YouTube playlist             │
    │   3. 🚪 Exit                                            │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
    """
    print(menu)


def print_quality_menu():
    """Print quality selection menu."""
    menu = """
    ┌─────────────────────────────────────────────────────────┐
    │                   SELECT QUALITY                        │
    ├─────────────────────────────────────────────────────────┤
    │                                                         │
    │   1. 360p    - Low quality (faster download)            │
    │   2. 720p    - HD quality (recommended)                 │
    │   3. 1080p   - Full HD quality                          │
    │   4. Best    - Best available quality                   │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
    """
    print(menu)


def print_download_type_menu():
    """Print download type menu."""
    menu = """
    ┌─────────────────────────────────────────────────────────┐
    │                  DOWNLOAD TYPE                          │
    ├─────────────────────────────────────────────────────────┤
    │                                                         │
    │   1. 🎬 Video + Audio (full video)                      │
    │   2. 🎵 Audio only (MP3 format)                         │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
    """
    print(menu)


def print_concurrent_menu():
    """Print concurrent download menu."""
    menu = """
    ┌─────────────────────────────────────────────────────────┐
    │              CONCURRENT DOWNLOADS                       │
    ├─────────────────────────────────────────────────────────┤
    │                                                         │
    │   Enable parallel downloading for playlists?            │
    │                                                         │
    │   1. 🚫 No (download one at a time)                     │
    │   2. 🚀 Yes (download multiple at once)                 │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
    """
    print(menu)


def get_input(prompt: str, valid_options: list = None) -> str:
    """Get user input with validation."""
    while True:
        user_input = input(f"\n{prompt}").strip()
        if valid_options:
            if user_input in valid_options:
                return user_input
            print(f"   ❌ Invalid input. Please enter: {', '.join(valid_options)}")
        else:
            return user_input


def main():
    """Main application entry point."""
    clear_screen()
    print_banner()

    downloader = YouTubeDownloader()

    while True:
        print_menu()
        choice = get_input("Enter your choice (1-3): ", ['1', '2', '3'])

        if choice == '3':
            print("\n👋 Thank you for using YouTube Downloader. Goodbye!\n")
            sys.exit(0)

        # Get URL
        print()
        url = get_input("Enter YouTube URL: ")

        if not url:
            print("   ❌ URL cannot be empty!")
            continue

        # Get quality
        clear_screen()
        print_banner()
        print_quality_menu()
        quality = get_input("Enter your choice (1-4): ", ['1', '2', '3', '4'])

        # Get download type
        clear_screen()
        print_banner()
        print_download_type_menu()
        download_type = get_input("Enter your choice (1-2): ", ['1', '2'])

        audio_only = download_type == '2'

        # Get concurrent downloads option (only for playlists)
        concurrent = 1
        if choice == '2':
            clear_screen()
            print_banner()
            print_concurrent_menu()
            concurrent_choice = get_input("Enable parallel downloads? (1-2): ", ['1', '2'])
            if concurrent_choice == '2':
                concurrent_str = get_input("How many concurrent downloads? (1-10): ", ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
                concurrent = int(concurrent_str)

        # Start download
        clear_screen()
        print_banner()

        if choice == '1':
            downloader.download_single_video(url, quality, audio_only)
        else:
            downloader.download_playlist(url, quality, audio_only, concurrent)

        # Ask if user wants to continue
        print()
        continue_choice = get_input("Download another? (y/n): ", ['y', 'n', 'Y', 'N'])
        if continue_choice.lower() != 'y':
            print("\n👋 Thank you for using YouTube Downloader. Goodbye!\n")
            sys.exit(0)

        clear_screen()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Download cancelled. Goodbye!\n")
        sys.exit(0)