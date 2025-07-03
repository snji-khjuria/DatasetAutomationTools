
import yt_dlp
import tempfile
import glob
import os
import shutil
from utils import sanitize_filename
from faster_whisper import WhisperModel

model_size="tiny"
model = WhisperModel(model_size)

ffmpeg_path = "C:/Program Files/ffmpeg-7.1.1-essentials_build/ffmpeg-7.1.1-essentials_build/bin/ffmpeg.exe"

def get_youtube_playlist_video_urls(playlist_url):
    ydl_opts = {'quiet': True, 'extract_flat': True, 'skip_download': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        return [entry['url'] for entry in info['entries'] if 'url' in entry]

#quality in ['320', '256', '192', '160', '128', '96', '64', '32']
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
                'preferredquality': '128',
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
    except Exception as e:
        print(f"Error transcribing video {video_url}: {e}")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
    return None, None


def prepare_youtube_dataset(dataset_location, youtube_playlists):
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
            if transcription is None or title is None:
                print(f"Failed to transcribe video: {url}")
                continue
            file_name = sanitize_filename(f"{playlist_name}_{title}", [])+".txt"
            # Clean up the title to make it suitable for a file name
            file_path = os.path.join(dataset_location, file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(transcription)
            print("video title:", title)
            print("transcription:", transcription[:100])