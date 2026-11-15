import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
from downloader import YouTubeDownloader
import i


class JustTubeApp(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.downloader = YouTubeDownloader()
        
        self.title("JustTube Downloader")
        self.geometry("550x440")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self._create_widgets()
        self._check_dependencies()

    def _check_dependencies(self):
        if not self.downloader.is_ffmpeg_installed():
            self.status_label.configure(
                text="Внимание: FFmpeg не найден! Конвертация в MP3 и 1080p+ могут не работать.",
                text_color="#FFA726"
            )

    def _create_widgets(self):
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=10, pady=(10, 0))

        self.settings_button = ctk.CTkButton(
            top_frame, text="⚙", font=ctk.CTkFont(size=14), width=32, height=32,
            command=self._open_settings
        )
        self.settings_button.pack(side="right", padx=(5, 0))

        self.aboutus_button = ctk.CTkButton(
            top_frame, text="ℹ", font=ctk.CTkFont(size=14), width=32, height=32,
            fg_color="#680000", hover_color="#8b0000",
            command=self._open_about
        )
        self.aboutus_button.pack(side="right")

        self.title_label = ctk.CTkLabel(
            self, text="JustTube Загрузчик", font=ctk.CTkFont(family="Arial", size=24, weight="bold")
        )
        self.title_label.pack(pady=(5, 2))

        self.version_label = ctk.CTkLabel(
            self, text=f'Версия: {i.version}', font=ctk.CTkFont(size=12), text_color="gray"
        )
        self.version_label.pack(pady=(0, 15))

        self.url_label = ctk.CTkLabel(self, text="Ссылка на YouTube видео:", font=ctk.CTkFont(size=13))
        self.url_label.pack(anchor="w", padx=45)
        
        self.url_input = ctk.CTkEntry(self, width=460, placeholder_text="https://youtu.be...", height=35)
        self.url_input.pack(pady=(5, 15), padx=45)

        self.path_label = ctk.CTkLabel(self, text="Путь для сохранения:", font=ctk.CTkFont(size=13))
        self.path_label.pack(anchor="w", padx=45)
        
        path_frame = ctk.CTkFrame(self, fg_color="transparent")
        path_frame.pack(pady=(5, 20), padx=45, fill="x")

        self.path_input = ctk.CTkEntry(path_frame, width=370, height=35)
        self.path_input.insert(0, self.downloader.default_path)
        self.path_input.pack(side="left", padx=(0, 10))

        self.browse_btn = ctk.CTkButton(
            path_frame, text="Обзор...", width=80, height=35, command=self._browse_folder
        )
        self.browse_btn.pack(side="right")

        self.download_btn = ctk.CTkButton(
            self, text="Скачать видео", font=ctk.CTkFont(size=14, weight="bold"),
            width=200, height=45, command=self._on_download_click
        )
        self.download_btn.pack(pady=5)

        self.progress_bar = ctk.CTkProgressBar(self, width=460, mode="determinate")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(15, 5))

        self.status_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12), justify="center", wraplength=460)
        self.status_label.pack(pady=5)

    def _browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.path_input.get())
        if folder:
            self.path_input.delete(0, "end")
            self.path_input.insert(0, folder)

    def _on_download_click(self):
        url = self.url_input.get().strip()
        if not url:
            self.status_label.configure(text="Ошибка: Введите ссылку!", text_color="#FF6B6B")
            return

        save_path = self.path_input.get().strip()

        self.download_btn.configure(state="disabled", text="Загрузка...")
        self.browse_btn.configure(state="disabled")
        self.progress_bar.set(0)
        self.status_label.configure(text="Получение информации о видео...", text_color="#FFFFFF")

        threading.Thread(target=self._async_download, args=(url, save_path), daemon=True).start()

    def _update_progress(self, value: float, status_text: str):
        self.after(0, lambda: self.progress_bar.set(value))
        self.after(0, lambda: self.status_label.configure(text=status_text, text_color="#FFFFFF"))

    def _async_download(self, url: str, save_path: str):
        try:
            actual_path = self.downloader.download_video(
                url, save_path, progress_callback=self._update_progress
            )
            self.after(0, lambda: self._on_download_success(actual_path))
        except Exception as e:
            err_msg = str(e)
            self.after(0, lambda: self._on_download_error(err_msg))

    def _on_download_success(self, actual_path: str):
        self.progress_bar.set(1.0)
        self.status_label.configure(text=f"Успешно сохранено в:\n{actual_path}", text_color="#4CAF50")
        self.url_input.delete(0, 'end')
        self._reset_controls()

    def _on_download_error(self, error_text: str):
        self.progress_bar.set(0)
        self.status_label.configure(text=f"Ошибка: {error_text}", text_color="#FF6B6B")
        self._reset_controls()

    def _reset_controls(self):
        self.download_btn.configure(state="normal", text="Скачать видео")
        self.browse_btn.configure(state="normal")

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
            text=f"JustTube Downloader {i.version}\n\nРазработчик: {i.author}\nGitHub: https://github.com/MrSashaman",
            font=ctk.CTkFont(size=13),
            justify="center"
        )
        info_label.pack(expand=True, pady=20)
        
        close_btn = ctk.CTkButton(about_window, text="Закрыть", width=100, command=about_window.destroy)
        close_btn.pack(pady=(0, 20))

    def _open_settings(self):
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Настройки")
        settings_window.geometry("520x350")  
        settings_window.resizable(False, False)
        settings_window.transient(self)
        settings_window.grab_set()


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
            ctk.CTkButton(
                formats_frame, 
                text=fmt.upper(), 
                font=ctk.CTkFont(size=11, weight="bold"), 
                width=75, 
                height=30,
                fg_color="#2c5c2e" if is_audio else None, 
                hover_color="#1e3d1f" if is_audio else None,
                command=lambda f=fmt: self._set_default_format(f)
            ).pack(side="left", padx=4)
