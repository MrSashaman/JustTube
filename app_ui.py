import os
import threading
import customtkinter as ctk
from downloader import YouTubeDownloader  
from tkinter import messagebox
import i

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
        self.settings_button = ctk.CTkButton(
            self, 
            text="⚙", 
            font=ctk.CTkFont(size=12), 
            width=30, 
            height=30, 
            command=self._open_settings
        )

        
        self.settings_button.pack(side="right", anchor="ne", pady=(5, 20), padx=(0, 10))


        self.aboutus_button = ctk.CTkButton(
            self, 
            text="🎲", 
            font=ctk.CTkFont(size=12), 
            width=30, 
            height=30, 
            fg_color="#680000",
            hover_color="#8b0000",
            command=self._open_about
        )
        self.aboutus_button.pack(side="right", anchor="ne", pady=(5, 20), padx=(0, 10))




        self.title_label = ctk.CTkLabel(self, text="JustTube Загрузчик", font=ctk.CTkFont(family="Arial", size=24, weight="bold"))
        self.title_label.pack(pady=(30, 20))

        self.version_label = ctk.CTkLabel(self, text=f'Версия: {i.version}', font=ctk.CTkFont(size=12))
        self.version_label.pack(pady=(0, 20))

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

    def _open_settings(self):
        self.settings_widget()

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

    def _set_default_format(self, fmt: str):
        self.downloader.current_format = fmt
        if hasattr(self, 'current_format_label'):
            self.current_format_label.configure(text=f"Текущий формат: {fmt.upper()}")

    def _open_about(self):
        about_window = ctk.CTkToplevel(self)
        about_window.title("О программе")
        about_window.geometry("350x200")
        about_window.resizable(False, False)
        
        about_window.transient(self)
        about_window.grab_set()
        
        info_label = ctk.CTkLabel(
            about_window, 
            text=f"JustTube Downloader {i.version}\n\nРазработчик: {i.author}\nGitHub: https://github.com/mrsashaman/JustTube",
            font=ctk.CTkFont(size=13),
            justify="center"
        )
        info_label.pack(expand=True, pady=20)
        
        close_btn = ctk.CTkButton(about_window, text="Закрыть", width=100, command=about_window.destroy)
        close_btn.pack(pady=(0, 20))


    def settings_widget(self):
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Настройки")
        settings_window.geometry("520x350")  
        settings_window.resizable(False, False)
        
        settings_window.transient(self)
        settings_window.grab_set()

        select_theme_label = ctk.CTkLabel(settings_window, text="Выберите тему приложения:", font=ctk.CTkFont(size=14, weight="bold"))
        select_theme_label.pack(pady=(20, 10))
        
        theme_frame = ctk.CTkFrame(settings_window, fg_color="transparent")
        theme_frame.pack(pady=5)
        
        dark_theme_button = ctk.CTkButton(theme_frame, text="Темная", font=ctk.CTkFont(size=12), width=100, height=30,
                                          command=lambda: ctk.set_appearance_mode("dark"))
        dark_theme_button.pack(side="left", padx=10)
        light_theme_button = ctk.CTkButton(theme_frame, text="Светлая", font=ctk.CTkFont(size=12), width=100, height=30,
                                           command=lambda: ctk.set_appearance_mode("light"))
        light_theme_button.pack(side="left", padx=10)

        hr_line = ctk.CTkFrame(settings_window, height=2, fg_color="gray30")
        hr_line.pack(fill="x", padx=20, pady=20)

        select_file_format_label = ctk.CTkLabel(settings_window, text="Выберите формат выходного файла (Видео / Аудио):", font=ctk.CTkFont(size=14, weight="bold"))
        select_file_format_label.pack(pady=(0, 5))
        
        self.current_format_label = ctk.CTkLabel(
            settings_window, 
            text=f"Текущий формат: {self.downloader.current_format.upper()}", 
            font=ctk.CTkFont(size=12),
            text_color="#4CAF50"
        )
        self.current_format_label.pack(pady=(0, 10))

        formats_frame = ctk.CTkFrame(settings_window, fg_color="transparent")
        formats_frame.pack(pady=5)

        list_of_formats = ['mp4', 'webm', 'mkv', 'avi', 'mp3', 'wav']
        for fmt in list_of_formats:
            is_audio = fmt in ['mp3', 'wav']
            
            format_button = ctk.CTkButton(
                formats_frame, 
                text=fmt.upper(), 
                font=ctk.CTkFont(size=11, weight="bold"), 
                width=75, 
                height=30,
                fg_color="#2c5c2e" if is_audio else None, 
                hover_color="#1e3d1f" if is_audio else None,
                command=lambda f=fmt: self._set_default_format(f)
            )
            format_button.pack(side="left", padx=4)
