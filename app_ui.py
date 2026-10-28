import os
import threading
import customtkinter as ctk
from downloader import YouTubeDownloader  

class JustTubeApp(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.downloader = YouTubeDownloader()
        
        self.title("JustTube Downloader")
        self.geometry("550x420")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self._create_widgets()

    def _create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="JustTube Загрузчик", font=ctk.CTkFont(family="Arial", size=24, weight="bold"))
        self.title_label.pack(pady=(30, 20))

        self.url_label = ctk.CTkLabel(self, text="Ссылка на YouTube видео:", font=ctk.CTkFont(size=13))
        self.url_label.pack(anchor="w", padx=45)
        
        self.url_input = ctk.CTkEntry(self, width=460, placeholder_text="https://youtu.be...", height=35)
        self.url_input.pack(pady=(5, 15), padx=45)

        self.path_label = ctk.CTkLabel(self, text="Путь для сохранения:", font=ctk.CTkFont(size=13))
        self.path_label.pack(anchor="w", padx=45)
        
        self.path_input = ctk.CTkEntry(self, width=460, height=35)
        self.path_input.insert(0, self.downloader.default_path)
        self.path_input.pack(pady=(5, 25), padx=45)

        self.download_btn = ctk.CTkButton(self, text="Скачать видео", font=ctk.CTkFont(size=14, weight="bold"), width=200, height=45, command=self._on_download_click)
        self.download_btn.pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(self, width=460, mode="indeterminate")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12), justify="center")
        self.status_label.pack(pady=10)

    def _on_download_click(self):
        url = self.url_input.get().strip()
        if not url:
            self.status_label.configure(text="Ошибка: Введите ссылку!", text_color="#FF6B6B")
            return

        save_path = self.path_input.get().strip()

        self.download_btn.configure(state="disabled", text="Загрузка...")
        self.progress_bar.set(0)
        self.progress_bar.start()
        self.status_label.configure(text="Анализ видео и скачивание...", text_color="#FFFFFF")

        threading.Thread(target=self._async_download, args=(url, save_path), daemon=True).start()

    def _async_download(self, url: str, save_path: str):
        try:
            actual_path = self.downloader.download_video(url, save_path)
            self.status_label.configure(text=f"Успешно сохранено в:\n{actual_path}", text_color="#4CAF50")
            self.url_input.delete(0, 'end')
        except Exception as e:
            self.status_label.configure(text=f"Ошибка: {e}", text_color="#FF6B6B")
        finally:
            self.progress_bar.stop()
            self.progress_bar.set(0)
            self.download_btn.configure(state="normal", text="Скачать видео")
