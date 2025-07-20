import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from utils.logger import log_event

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".7z", ".tar"]
}

class DownloadSorterUI:
    def __init__(self, root, parent_frame):
        self.frame = tk.Frame(parent_frame, bg="#ecf0f1", padx=20, pady=20)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="🗂️ Download Folder Sorter", font=("Arial", 14, "bold"), bg="#ecf0f1").pack(anchor="w", pady=(0, 10))

        # 📁 Choose folder
        tk.Label(self.frame, text="Choose folder to sort:", bg="#ecf0f1").pack(anchor="w")
        self.folder_var = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        tk.Entry(self.frame, textvariable=self.folder_var, width=60).pack(anchor="w")
        tk.Button(self.frame, text="📁 Browse", command=self.browse_folder).pack(pady=5, anchor="w")

        # 🔘 Sort button
        tk.Button(self.frame, text="🚀 Sort Files", bg="#3498db", fg="white", command=self.sort_files).pack(pady=10, anchor="w")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)

    def sort_files(self):
        folder = self.folder_var.get().strip()
        if not os.path.isdir(folder):
            messagebox.showerror("Invalid Path", "Please select a valid folder.")
            return

        try:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    ext = os.path.splitext(filename)[1].lower()
                    for category, extensions in FILE_TYPES.items():
                        if ext in extensions:
                            target_folder = os.path.join(folder, category)
                            os.makedirs(target_folder, exist_ok=True)
                            shutil.move(file_path, os.path.join(target_folder, filename))
                            break

            messagebox.showinfo("Done", "🎉 Files sorted successfully!")
            log_event("Download Sorter", f"Sorted files in: {folder}")

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong: {e}")
