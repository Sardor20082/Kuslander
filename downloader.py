import yt_dlp
import tempfile

def download_video(url: str):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': temp_file.name,
        'quiet': True,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return temp_file.name, temp_file.name.split("/")[-1]
