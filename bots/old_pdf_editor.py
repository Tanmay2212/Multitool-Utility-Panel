import os
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from threading import Thread
from utils.logger import log_event


class PDFEditorUI:
    def __init__(self, root, parent_frame):
        self.root = root
        self.frame = tk.Frame(parent_frame, bg="#f4f6f7", padx=10, pady=10)
        self.frame.pack(fill="both", expand=True)

        self.pdf_path = ""
        self.doc = None
        self.erasing = False
        self.erase_coords = []

        # Toolbar
        self.toolbar = tk.Frame(self.frame, bg="#dfe6e9")
        self.toolbar.pack(fill="x", pady=5)

        tk.Button(self.toolbar, text="📁 Upload PDF", command=self.upload_pdf).pack(side="left", padx=4)
        tk.Button(self.toolbar, text="👁️ Preview", command=self.preview_text).pack(side="left", padx=4)
        tk.Button(self.toolbar, text="🧽 Erase Logos", command=self.toggle_eraser).pack(side="left", padx=4)
        tk.Button(self.toolbar, text="🔁 Replace Text", command=self.start_replace_thread).pack(side="left", padx=4)
        tk.Button(self.toolbar, text="💾 Save PDF", command=self.save_pdf).pack(side="left", padx=4)

        # Page Info
        self.page_label = tk.Label(self.frame, text="", bg="#f4f6f7")
        self.page_label.pack(anchor="w")

        # Text Replacement UI
        self.old_text_var = tk.StringVar()
        self.new_text_var = tk.StringVar()

        form = tk.Frame(self.frame, bg="#f4f6f7")
        form.pack(anchor="w", pady=10)

        tk.Label(form, text="Find:", bg="#f4f6f7").grid(row=0, column=0, sticky="w")
        tk.Entry(form, textvariable=self.old_text_var, width=30).grid(row=0, column=1, padx=5)

        tk.Label(form, text="Replace with:", bg="#f4f6f7").grid(row=1, column=0, sticky="w")
        tk.Entry(form, textvariable=self.new_text_var, width=30).grid(row=1, column=1, padx=5)

        # Progress + Status
        self.progress = ttk.Progressbar(self.frame, length=300, mode="determinate")
        self.progress.pack(anchor="w", pady=5)

        self.status_var = tk.StringVar()
        tk.Label(self.frame, textvariable=self.status_var, bg="#f4f6f7", fg="black", font=("Arial", 10)).pack(anchor="w")

    def upload_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if path:
            try:
                self.doc = fitz.open(path)
                self.pdf_path = path
                self.page_label.config(text=f"📄 Total Pages: {len(self.doc)}")
                self.status_var.set("✅ PDF Loaded")
                log_event("PDF Editor", f"Loaded: {path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load PDF: {e}")

    def preview_text(self):
        if not self.doc:
            return
        preview_window = tk.Toplevel(self.root)
        preview_window.title("📝 PDF Text Preview")
        preview_window.geometry("800x600")
        text_area = tk.Text(preview_window, wrap="word")
        text_area.pack(fill="both", expand=True)
        full_text = ""
        for page in self.doc:
            full_text += f"\n--- Page {page.number + 1} ---\n"
            full_text += page.get_text()
        text_area.insert("1.0", full_text)

    def toggle_eraser(self):
        if not self.doc:
            messagebox.showwarning("No PDF", "Please upload a PDF first.")
            return
        self.status_var.set("🧽 Eraser Active: Drag on the image to whiteout (first page only)")
        self.show_first_page_canvas()

    def show_first_page_canvas(self):
        window = tk.Toplevel(self.root)
        window.title("🧽 Drag to erase logo/image")

        canvas = tk.Canvas(window, width=600, height=800, bg="white")
        canvas.pack(fill="both", expand=True)

        page = self.doc[0]
        pix = page.get_pixmap(dpi=100)
        img_path = "temp_page.png"
        pix.save(img_path)
        self.bg_img = tk.PhotoImage(file=img_path)
        canvas.create_image(0, 0, anchor="nw", image=self.bg_img)

        self.start_x, self.start_y = 0, 0

        def start_drag(event):
            self.start_x, self.start_y = event.x, event.y
            self.drag_rect = canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

        def drag_motion(event):
            canvas.coords(self.drag_rect, self.start_x, self.start_y, event.x, event.y)

        def finish_drag(event):
            x0, y0, x1, y1 = canvas.coords(self.drag_rect)
            page.draw_rect(fitz.Rect(x0, y0, x1, y1), color=(1, 1, 1), fill=(1, 1, 1))
            self.status_var.set("✅ Erased selected region")
            window.destroy()

        canvas.bind("<Button-1>", start_drag)
        canvas.bind("<B1-Motion>", drag_motion)
        canvas.bind("<ButtonRelease-1>", finish_drag)

    def start_replace_thread(self):
        Thread(target=self.replace_text).start()

    def replace_text(self):
        if not self.doc:
            messagebox.showerror("Error", "Upload a PDF first.")
            return

        old = self.old_text_var.get()
        new = self.new_text_var.get()

        if not old:
            messagebox.showwarning("Missing", "Enter the text to find.")
            return

        self.status_var.set("🔁 Replacing...")
        total_pages = len(self.doc)

        for i, page in enumerate(self.doc):
            blocks = page.get_text("dict")["blocks"]
            for b in blocks:
                for line in b.get("lines", []):
                    for span in line.get("spans", []):
                        if old in span["text"]:
                            rect = fitz.Rect(span["bbox"])
                            page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                            updated_text = span["text"].replace(old, new)
                            page.insert_textbox(rect, updated_text,
                                                fontsize=span["size"],
                                                fontname=span["font"],
                                                color=(0, 0, 0),
                                                align=0)

            self.progress["value"] = ((i + 1) / total_pages) * 100

        self.status_var.set("✅ Replacement done. Use Save to export.")

    def save_pdf(self):
        if not self.doc:
            messagebox.showwarning("Nothing to save", "Upload and modify a PDF first.")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if save_path:
            self.doc.save(save_path)
            self.status_var.set("✅ PDF Saved Successfully!")
            log_event("PDF Editor", f"Saved PDF to {save_path}")
        else:
            self.status_var.set("❌ Save Cancelled.")
