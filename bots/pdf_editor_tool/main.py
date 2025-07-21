import os
import tkinter as tk
from tkinter import filedialog, messagebox
from .utils.reader import extract_text_with_font
from .utils.selector import show_selector_ui
from .utils.replacer import replace_text_in_pdf

backup_dir = "backups"
os.makedirs(backup_dir, exist_ok=True)

class PDFEditorApp:
    def __init__(self, root, container=None):
        self.root = root
        self.frame = container or root

        self.pdf_path = None
        self.pdf_text = []
        self.undo_stack = []
        self.redo_stack = []
        self.modified_pdf = None
        self.last_highlight = None  # 🟡 new

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.frame, text="🧠 Welcome to PDF Editor Tool", font=("Helvetica", 18, "bold"), fg="#2d3436", bg="#ffffff").pack(pady=10)

        top_frame = tk.Frame(self.frame, bg="#ffffff")
        top_frame.pack(fill="x", padx=10, pady=5)

        tk.Button(top_frame, text="📁 Load PDF", command=self.load_pdf, bg="#0984e3", fg="white").pack(side="left", padx=5)
        tk.Button(top_frame, text="↩️ Undo", command=self.undo, bg="#636e72", fg="white").pack(side="left", padx=5)
        tk.Button(top_frame, text="↪️ Redo", command=self.redo, bg="#636e72", fg="white").pack(side="left", padx=5)
        tk.Button(top_frame, text="💾 Save", command=self.save_pdf, bg="#00b894", fg="white").pack(side="right", padx=5)

        replace_frame = tk.Frame(self.frame, bg="#f1f2f6")
        replace_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(replace_frame, text="Find:", bg="#f1f2f6").pack(side="left")
        self.old_entry = tk.Entry(replace_frame, width=20)
        self.old_entry.pack(side="left", padx=5)

        tk.Label(replace_frame, text="Replace With:", bg="#f1f2f6").pack(side="left")
        self.new_entry = tk.Entry(replace_frame, width=20)
        self.new_entry.pack(side="left", padx=5)

        tk.Button(replace_frame, text="🔁 Replace Text", command=self.replace_text, bg="#fdcb6e").pack(side="left", padx=5)

        self.status_var = tk.StringVar()
        tk.Label(self.frame, textvariable=self.status_var, anchor="w", bg="white").pack(fill="x", padx=10)

        self.text_area = tk.Text(self.frame, wrap="word", bg="white")
        self.text_area.pack(fill="both", expand=True, padx=10, pady=10)

        self.text_area.tag_config("highlight", background="yellow", foreground="black")

    def load_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not path:
            return
        try:
            self.pdf_path = path
            self.modified_pdf = None
            self.pdf_text = extract_text_with_font(path)
            self.show_preview()
            self.status_var.set("✅ PDF Loaded")

            backup_path = os.path.join(backup_dir, os.path.basename(path))
            with open(path, "rb") as f_src, open(backup_path, "wb") as f_bak:
                f_bak.write(f_src.read())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load PDF: {e}")

    def show_preview(self, highlight_word=""):
        self.text_area.config(state="normal")
        self.text_area.delete("1.0", "end")

        old = highlight_word.lower() if highlight_word else self.old_entry.get().strip().lower()

        for page_index, page_data in enumerate(self.pdf_text):
            self.text_area.insert("end", f"\n📄 ChatGPT PDF Style - Page {page_index + 1}\n", "header")

            for span in page_data:
                line = span["text"]

                if old and old in line.lower():
                    start_idx = self.text_area.index("end-1c")
                    self.text_area.insert("end", line + "\n")
                    end_idx = self.text_area.index("end-1c")
                    self.text_area.tag_add("highlight", start_idx, end_idx)
                else:
                    self.text_area.insert("end", line + "\n")

        self.text_area.tag_config("highlight", background="#fff9c4", foreground="black")
        self.text_area.tag_config("header", foreground="#00b894", font=("Helvetica", 12, "bold"))

        self.text_area.config(state="disabled")


    def replace_text(self):
        if not self.pdf_path:
            messagebox.showwarning("Load First", "Please load a PDF file.")
            return

        old = self.old_entry.get().strip()
        new = self.new_entry.get().strip()

        if not old or not new:
            self.status_var.set("⚠️ Please enter both words.")
            return

        matches = []
        for page_index, lines in enumerate(self.pdf_text):
            for span in lines:
                if old.lower() in span["text"].lower():
                    matches.append({
                        "page": page_index,
                        "text": span["text"],
                        "bbox": span["bbox"],
                        "font": span["font"],
                        "size": span["size"]
                    })

        if not matches:
            self.status_var.set(f"⚠️ No matches found for '{old}'")
            return

        selected = show_selector_ui(self.frame, matches, old)
        if not selected:
            self.status_var.set("⚠️ No matches selected.")
            return

        self.undo_stack.append((self.pdf_text.copy(), f"Undo '{old}' → '{new}'"))

        try:
            doc = replace_text_in_pdf(self.pdf_path, selected, old, new)
            self.modified_pdf = doc

            preview_path = self.pdf_path.replace(".pdf", "_preview.pdf")
            doc.save(preview_path)
            self.pdf_path = preview_path
            self.pdf_text = extract_text_with_font(preview_path)
            self.show_preview(highlight_word=new)
            self.status_var.set(f"✅ Replaced '{old}' → '{new}'. Click 💾 Save to export.")
        except Exception as e:
            messagebox.showerror("Replace Error", f"Replacement failed: {e}")

    def undo(self):
        if not self.undo_stack:
            self.status_var.set("⚠️ Nothing to undo.")
            return
        self.redo_stack.append((self.pdf_text.copy(), "Redo"))
        self.pdf_text, _ = self.undo_stack.pop()
        self.show_preview()
        self.status_var.set("↩️ Undone")

    def redo(self):
        if not self.redo_stack:
            self.status_var.set("⚠️ Nothing to redo.")
            return
        self.undo_stack.append((self.pdf_text.copy(), "Undo"))
        self.pdf_text, _ = self.redo_stack.pop()
        self.show_preview()
        self.status_var.set("↪️ Redone")

    def save_pdf(self):
        if not self.modified_pdf:
            messagebox.showwarning("No Edits", "No updated PDF to save.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if path:
            try:
                self.modified_pdf.save(path)
                self.status_var.set(f"✅ Saved as {os.path.basename(path)}")
                messagebox.showinfo("Saved", f"PDF saved successfully at:\n{path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save: {e}")
