import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from yt_dlp import YoutubeDL
from threading import Thread
from utils.logger import log_event
class YouTubeDownloaderUI:
    def __init__(self, root, parent_frame):  # <-- Accept 2 args
        self.root = root
        self.cancelled = False
        self.frame = tk.Frame(parent_frame, bg="#ecf0f1", padx=20, pady=20)
        self.frame.pack(fill="both", expand=True)


        tk.Label(self.frame, text="📥 YouTube Downloader", font=("Arial", 14, "bold"), bg="#ecf0f1").pack(anchor="w")

        # URL input
        tk.Label(self.frame, text="Paste YouTube Link:", bg="#ecf0f1").pack(anchor="w", pady=(10, 0))
        self.link_var = tk.StringVar()
        tk.Entry(self.frame, textvariable=self.link_var, width=60).pack(pady=5, anchor="w")

        # Type selection
        tk.Label(self.frame, text="Select Type:", bg="#ecf0f1").pack(anchor="w")
        self.download_type = tk.StringVar(value="video")
        tk.Radiobutton(self.frame, text="🎥 Video (MP4)", variable=self.download_type, value="video", bg="#ecf0f1").pack(anchor="w")
        tk.Radiobutton(self.frame, text="🎵 Audio (MP3)", variable=self.download_type, value="audio", bg="#ecf0f1").pack(anchor="w")

        # Save folder
        tk.Label(self.frame, text="Save to Folder:", bg="#ecf0f1").pack(anchor="w", pady=(10, 0))
        self.folder_var = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        tk.Entry(self.frame, textvariable=self.folder_var, width=60).pack(anchor="w")
        tk.Button(self.frame, text="📁 Browse", command=self.browse_folder).pack(pady=5, anchor="w")

        # Progress bar
        self.progress = ttk.Progressbar(self.frame, length=400, mode="determinate")
        self.progress.pack(pady=(10, 5), anchor="w")

        # Status label
        self.status_var = tk.StringVar()
        tk.Label(self.frame, textvariable=self.status_var, bg="#ecf0f1", font=("Arial", 10, "italic")).pack(anchor="w")

        # Action buttons
        btn_frame = tk.Frame(self.frame, bg="#ecf0f1")
        btn_frame.pack(pady=10, anchor="w")
        tk.Button(btn_frame, text="🚀 Download", bg="#27ae60", fg="white", command=self.start_download_thread).pack(side="left", padx=5)
        tk.Button(btn_frame, text="❌ Cancel", bg="#c0392b", fg="white", command=self.cancel_download).pack(side="left", padx=5)

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_var.set(path)

    def cancel_download(self):
        self.cancelled = True
        self.status_var.set("❌ Cancelled by user.")

    def start_download_thread(self):
        self.cancelled = False
        Thread(target=self.download_video).start()

    def download_video(self):
        link = self.link_var.get().strip()
        folder = self.folder_var.get().strip()
        mode = self.download_type.get()

        if not link:
            messagebox.showerror("Error", "Please enter a YouTube link.")
            return

        self.status_var.set("⏳ Starting download...")
        self.progress["value"] = 0

        # Hook for download progress
        def hook(d):
            if self.cancelled:
                raise Exception("Download cancelled")

            if d["status"] == "downloading":
                percent = d.get("_percent_str", "0%").strip().replace('%', '')
                try:
                    self.progress["value"] = float(percent)
                except:
                    pass
                self.status_var.set(f"⬇️ Downloading... {percent}%")

            elif d["status"] == "finished":
                self.progress["value"] = 100
                self.status_var.set("✅ Download completed")
                log_event("YouTube Downloader", "Download completed.")


        try:
            opts = {
                "progress_hooks": [hook],
                "outtmpl": os.path.join(folder, "%(title)s.%(ext)s"),
                "noplaylist": True  # force ignore playlist
            }

            if mode == "audio":
                opts.update({
                    "format": "bestaudio/best",
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }],
                })
            else:
                opts.update({
                    "format": "bestvideo+bestaudio/best",
                    "merge_output_format": "mp4",
                })

            with YoutubeDL(opts) as ydl:
                ydl.download([link])

        except Exception as e:
            self.status_var.set(f"❌ Error: {e}")
