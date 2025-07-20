import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from utils.logger import log_event

class ImageToPDFUI:
    def __init__(self, root, parent_frame):
        self.root = root
        self.image_paths = []

        self.frame = tk.Frame(parent_frame, bg="#ecf0f1", padx=20, pady=20)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="🖼️ Image to PDF Converter", font=("Arial", 14, "bold"), bg="#ecf0f1").pack(anchor="w", pady=(0, 10))

        # Select images
        tk.Button(self.frame, text="📂 Select Images (max 20)", command=self.select_images).pack(anchor="w", pady=5)
        self.selected_listbox = tk.Listbox(self.frame, width=80, height=10)
        self.selected_listbox.pack(pady=10)

        # Save location
        tk.Label(self.frame, text="Save PDF to Folder:", bg="#ecf0f1").pack(anchor="w", pady=(10, 0))
        self.folder_var = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        tk.Entry(self.frame, textvariable=self.folder_var, width=60).pack(anchor="w")
        tk.Button(self.frame, text="📁 Browse", command=self.browse_folder).pack(pady=5, anchor="w")

        # Output filename
        tk.Label(self.frame, text="PDF File Name:", bg="#ecf0f1").pack(anchor="w", pady=(10, 0))
        self.pdf_name_entry = tk.Entry(self.frame, width=40)
        self.pdf_name_entry.pack(anchor="w")

        # Convert button
        tk.Button(self.frame, text="📄 Convert to PDF", bg="#27ae60", fg="white", command=self.convert_to_pdf).pack(pady=15)

    def select_images(self):
        paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if len(paths) > 20:
            messagebox.showerror("Limit Exceeded", "Select up to 20 images only.")
            return

        self.image_paths = paths
        self.selected_listbox.delete(0, tk.END)
        for path in paths:
            self.selected_listbox.insert(tk.END, os.path.basename(path))

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_var.set(path)

    def convert_to_pdf(self):
        if not self.image_paths:
            messagebox.showwarning("No Images", "Please select some images first.")
            return

        pdf_name = self.pdf_name_entry.get().strip()
        if not pdf_name:
            messagebox.showwarning("No Name", "Please enter a PDF file name.")
            return

        save_folder = self.folder_var.get().strip()
        output_path = os.path.join(save_folder, pdf_name + ".pdf")

        try:
            images = []
            for path in self.image_paths:
                img = Image.open(path).convert("RGB")
                images.append(img)

            images[0].save(output_path, save_all=True, append_images=images[1:])
            messagebox.showinfo("Success", f"PDF saved to: {output_path}")
            log_event("Image to PDF", f"Created PDF: {output_path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))
