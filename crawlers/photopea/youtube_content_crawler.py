import sys
import os
import asyncio
from crawl4ai.async_configs import CrawlerRunConfig


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from crawlers.utils import get_youtube_playlist_video_urls, transcribe_youtube_audio_direct, sanitize_filename


youtube_playlists = [("fNd", "https://www.youtube.com/playlist?list=PLvNXvOQ8ylUU9C7gzA1Xtg79KBmlAKghh"),
                     ("techSupport", "https://www.youtube.com/playlist?list=PLqWGp356JsNvKFTNgvvNfYfVdOs_M9EYv"),
                     ("kruMark", "https://www.youtube.com/playlist?list=PL5fmsRtjcmExeJFmoBsTtFL0vnj4g5xj7"),
                     ("Adomi", "https://www.youtube.com/playlist?list=PLCMGVxg-SSzV30nX9HWAIAacfY6-gHDdR"),
                     ("Auri", "https://www.youtube.com/playlist?list=PLWo9muNw-oVRujzM_sF2TnIEz_4sQsAL-"),
                     ("Cambit", "https://www.youtube.com/playlist?list=PLwkbAxcLGld2hVwe0Kt_t358E4z_E2bE8")]

dataset_location = "./datasets/photopea/youtube_transcriptions"
if os.path.exists(dataset_location):
    import shutil
    shutil.rmtree(dataset_location)
os.makedirs(dataset_location, exist_ok=True)


for playlist_name, playlist_url in youtube_playlists:
    print(f"Processing playlist: {playlist_name} ({playlist_url})")
    video_urls = get_youtube_playlist_video_urls(playlist_url)
    print(f"Found {len(video_urls)} videos in {playlist_name}:")

    for url in video_urls:
        print("url:", url)
        transcription, title = transcribe_youtube_audio_direct(url)
        file_name = sanitize_filename(f"{playlist_name}_{title}", [])+".txt"
        # Clean up the title to make it suitable for a file name
        file_path = os.path.join(dataset_location, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(transcription)
        print("video title:", title)
        print("transcription:", transcription[:100])