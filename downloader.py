import os
import yt_dlp
import getraw

class YouTubeDownloader:
    
    def __init__(self, default_path: str = None):
        self.default_path = default_path or os.getcwd()

    def download_video(self, url: str, save_path: str = None) -> str:
        target_path = save_path.strip() if save_path else self.default_path
        target_path = os.path.expanduser(target_path)
        
        os.makedirs(target_path, exist_ok=True)
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(target_path, '%(title)s.%(ext)s'),
            'js_runtimes': {
                'deno': {}, 
                'node': {}
            }, 
            'remote_components': 'ejs:github',
            'extractor_args': {
                'youtube': {
                    'skip': ['js'],
                    'player_client': ['mweb', 'tv_embedded', 'default']
                }
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        try:
            json_log_path = os.path.join(target_path, "os_raw_data.json")
            getraw.save_raw_os_data(json_log_path)
        except Exception as json_error:
            print(f"[Ошибка записи JSON]: {json_error}")
                
        return target_path

