# SoftwareAutomation Project

This project provides tools for automating the crawling, downloading, and transcription of web and YouTube content. It is organized into several modules for different automation tasks.

## Features

- **Web Crawling**: Extracts and scrapes URLs and content from websites using `crawl4ai`.
- **YouTube Playlist Transcription**: Downloads audio from all videos in a playlist and transcribes them using OpenAI Whisper models.
- **Dataset Management**: Organizes and stores crawled and transcribed data for further processing.

## Directory Structure

```
requirements.txt
configs/
crawlers/
    utils.py
    photopea/
        documentation_crawler.py
        pdf_dataset_downloader.py
    youtube_playlist_transcriber.py
    url_crawler.py
datasets/
    ...
```

## Installation

1. Clone the repository or download the project files.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   Or, manually install:
   ```sh
   pip install gdown
   pip install -U crawl4ai
   pip install pytube
   pip install openai-whisper
   ```

## Usage

### 1. Web Crawling
- Example: Extract and print all internal and external links from a page.
  ```sh
  python -m crawlers.photopea.documentation_crawler
  ```

### 2. YouTube Playlist Transcription
- Download and transcribe all videos in a playlist:
  ```sh
  python crawlers/youtube_playlist_transcriber.py
  ```
  - Enter the playlist URL and select Whisper models as prompted.

### 3. URL Crawler
- Extract and scrape all URLs from a given page:
  ```sh
  python crawlers/url_crawler.py
  ```

## Notes
- For module imports to work, run scripts from the project root or use the `-m` flag as shown above.
- Output data is saved in organized folders under `datasets/` or `transcriptions/`.

## Requirements
- Python 3.8+
- See `requirements.txt` for dependencies.