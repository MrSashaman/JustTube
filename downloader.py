import os
import shutil
import yt_dlp


class YouTubeDownloader:
    
    def __init__(self, default_path: str = None):
        self.default_path = default_path or os.path.join(os.path.expanduser("~"), "Downloads")
        self.current_format = 'mp4'

    @staticmethod
    def is_ffmpeg_installed() -> bool:
        return shutil.which("ffmpeg") is not None

    def download_video(self, url: str, save_path: str = None, progress_callback=None) -> str:
        target_path = save_path.strip() if save_path else self.default_path
        target_path = os.path.expanduser(target_path)
        os.makedirs(target_path, exist_ok=True)

        def _hook(d):
            if progress_callback and d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                if total:
                    percent = downloaded / total
                    speed = d.get('_speed_str', '').strip()
                    progress_callback(percent, f"Загрузка: {percent * 100:.1f}% ({speed})")
            elif progress_callback and d['status'] == 'finished':
                progress_callback(1.0, "Обработка и склейка файлов...")

        ydl_opts = {
            'progress_hooks': [_hook],
            'noplaylist': True,  
            'quiet': True,
            'no_warnings': True,
        }

        if self.current_format in ['mp3', 'wav']:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(target_path, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': self.current_format,
                    'preferredquality': '192',
                }],
            })
        else:
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': os.path.join(target_path, f'%(title)s.{self.current_format}'),
                'merge_output_format': self.current_format,
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return target_path
