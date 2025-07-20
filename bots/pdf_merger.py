import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
from utils.logger import log_event

class PDFMergerUI:
    def __init__(self, root, parent_frame):
        self.root = root
        self.files = []

        self.frame = tk.Frame(parent_frame, bg="#ecf0f1", padx=20, pady=20)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="🧩 PDF Merger", font=("Arial", 14, "bold"), bg="#ecf0f1").pack(anchor="w")

        tk.Button(self.frame, text="➕ Add PDF Files", command=self.add_files).pack(anchor="w", pady=(10, 5))
        self.listbox = tk.Listbox(self.frame, width=60, height=10)
        self.listbox.pack()

        tk.Button(self.frame, text="🧠 Merge Now", command=self.merge_pdfs, bg="#27ae60", fg="white").pack(anchor="w", pady=(10, 15))

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        for f in files:
            if f not in self.files:
                self.files.append(f)
                self.listbox.insert(tk.END, os.path.basename(f))

    def merge_pdfs(self):
        if not self.files:
            messagebox.showerror("Error", "No PDFs selected.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF File", "*.pdf")])
        if not save_path:
            return

        try:
            merger = PdfMerger()
            for f in self.files:
                merger.append(f)
            merger.write(save_path)
            merger.close()

            log_event("PDF Merger", f"Merged {len(self.files)} files into {save_path}")
            messagebox.showinfo("Success", f"PDFs merged successfully:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
