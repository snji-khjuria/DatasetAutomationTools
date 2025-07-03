import asyncio
from crawl4ai import AsyncWebCrawler
from urllib.parse import urlparse
import re
import os
import asyncio
import shutil
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
import os
import shutil
import gdown
import yt_dlp
import tempfile
import glob

from faster_whisper import WhisperModel

model_size="tiny"
model = WhisperModel(model_size)

ffmpeg_path = "C:/Program Files/ffmpeg-7.1.1-essentials_build/ffmpeg-7.1.1-essentials_build/bin/ffmpeg.exe"
def extract_urls(url, url_info):
    approved_prefix, banned_urls = url_info
    """Extract all URLs from a given web page using crawl4ai."""
    async def _extract():
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            links = result.links
            if not links:
                print(f"No links found on the page: {url}")
                return []
            internal_links = [k["href"] for k in links.get("internal", []) if k["href"].startswith(approved_prefix)]
            external_links = [k["href"] for k in links.get("external", []) if k["href"].startswith(approved_prefix)]
            total_urls = internal_links + external_links
            total_urls = [url for url in total_urls if url not in banned_urls]
            return list(set(total_urls))
    return asyncio.run(_extract())



def sanitize_filename(url, removable_prefix_list):
    #remove prefix if present from any of the removable prefixes_list
    for prefix in removable_prefix_list:
        if url.startswith(prefix):
            url = url[len(prefix):]
    # Replace all non-alphanumeric characters with underscores
    return re.sub(r'[^a-zA-Z0-9]', '_', url)




async def save_text_from_url(url, removable_prefix_list, output_dir, crawler=None, run_config=None):
    try:
        result = await crawler.arun(url=url, config=run_config)
        text = result.markdown
    except Exception as e:
        print(f"❌ Failed to load {url}: {e}")
        return

    filename = sanitize_filename(url, removable_prefix_list) + ".txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"✅ Saved: {filepath}")



async def process_url_list(url_list, removable_prefix_list, run_config, output_dir):
    browser_config = BrowserConfig()

    # Remove entire output directory if it exists
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    async with AsyncWebCrawler(config=browser_config) as crawler:
        tasks = [save_text_from_url(url, removable_prefix_list, output_dir, crawler, run_config) for url in url_list]
        await asyncio.gather(*tasks)



def download_drive_folder(drive_url: str, local_folder: str):
    # Delete the folder if it exists
    if os.path.exists(local_folder):
        shutil.rmtree(local_folder)
    os.makedirs(local_folder, exist_ok=True)

    # Extract folder ID from the Google Drive folder URL
    if "folders/" in drive_url:
        folder_id = drive_url.split("folders/")[1].split("?")[0]
    else:
        raise ValueError("Invalid folder link. Must be of the form: https://drive.google.com/drive/folders/<FOLDER_ID>")

    # gdown format to download folders
    gdown.download_folder(f"https://drive.google.com/drive/folders/{folder_id}", output=local_folder, quiet=False, use_cookies=False)

    print(f"All files downloaded to: {local_folder}")



def get_youtube_playlist_video_urls(playlist_url):
    ydl_opts = {'quiet': True, 'extract_flat': True, 'skip_download': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        return [entry['url'] for entry in info['entries'] if 'url' in entry]

def transcribe_youtube_audio_direct(video_url):
    tmp_dir = tempfile.mkdtemp()

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': os.path.join(tmp_dir, "%(title).128s.%(ext)s"),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        if ffmpeg_path:
            ydl_opts['ffmpeg_location'] = ffmpeg_path

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            title = info.get('title', 'untitled').replace("/", "_").replace("\\", "_")

        mp3_files = glob.glob(os.path.join(tmp_dir, "*.mp3"))
        if not mp3_files:
            raise RuntimeError("MP3 file not found after download.")

        mp3_path = mp3_files[0]

        # Use faster-whisper: returns (segments, info)
        segments, _ = model.transcribe(mp3_path)

        transcript = "".join([segment.text.strip() + "\n" for segment in segments])

        return transcript, title

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)