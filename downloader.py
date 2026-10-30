import os
import yt_dlp

class YouTubeDownloader:
    
    def __init__(self, default_path: str = None):
        self.default_path = default_path or os.getcwd()
        self.current_format = 'mp4'
    def download_video(self, url: str, save_path: str = None) -> str:
        target_path = save_path.strip() if save_path else self.default_path
        target_path = os.path.expanduser(target_path)
        
        os.makedirs(target_path, exist_ok=True)
        
        ydl_opts = {
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
