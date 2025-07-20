import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader
from transformers import pipeline
import threading
from utils.logger import log_event

class PDFSummarizerUI:
    def __init__(self, root, parent_frame):
        self.frame = tk.Frame(parent_frame, bg="#f4f4f4", padx=20, pady=20)
        self.frame.pack(fill="both", expand=True)

        tk.Label(
            self.frame, text="📄 PDF Summarizer (Offline AI)",
            font=("Segoe UI", 16, "bold"), bg="#f4f4f4", fg="#2c3e50"
        ).pack(anchor="w", pady=(0, 15))

        tk.Button(
            self.frame, text="📂 Select PDF File",
            command=self.load_pdf,
            font=("Segoe UI", 11), bg="#3498db", fg="white",
            activebackground="#2980b9", relief="flat", padx=10, pady=6
        ).pack(anchor="w")

        # Summary box
        self.summary_box = tk.Text(self.frame, wrap="word", height=25, font=("Segoe UI", 11))
        self.summary_box.pack(fill="both", expand=True, pady=(15, 5))

        # Buttons below summary
        button_frame = tk.Frame(self.frame, bg="#f4f4f4")
        button_frame.pack(anchor="e", pady=5)

        tk.Button(
            button_frame, text="📋 Copy to Clipboard",
            command=self.copy_to_clipboard,
            bg="#27ae60", fg="white", padx=10, pady=4,
            activebackground="#1e8449", relief="flat"
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame, text="💾 Export Summary",
            command=self.export_summary,
            bg="#e67e22", fg="white", padx=10, pady=4,
            activebackground="#ca6f1e", relief="flat"
        ).pack(side="left", padx=5)

    def load_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not path:
            return

        self.summary_box.delete("1.0", tk.END)
        self.summary_box.insert(tk.END, "⏳ Please wait... summarizing the document...\n")

        threading.Thread(target=self.process_pdf, args=(path,), daemon=True).start()

    def format_summary(self, summaries):
        formatted = "📘 Summary Report\n\n"
        for i, summary in enumerate(summaries, 1):
            formatted += f"📝 Section {i}:\n{summary.strip()}\n\n"
        return formatted

    def process_pdf(self, path):
        try:
            reader = PdfReader(path)
            full_text = ""
            for page in reader.pages[:5]:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

            summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=-1)

            chunks = [full_text[i:i+1000] for i in range(0, len(full_text), 1000)]
            summaries = []

            for chunk in chunks:
                try:
                    result = summarizer(chunk, max_length=120, min_length=40, do_sample=False)[0]
                    summaries.append(result["summary_text"])
                except Exception as chunk_err:
                    summaries.append(f"❗ Error summarizing chunk: {chunk_err}")

            final_summary = self.format_summary(summaries)

            self.summary_box.delete("1.0", tk.END)
            self.summary_box.insert(tk.END, final_summary)
            log_event("PDF Summarizer", f"Summarized: {os.path.basename(path)}")

        except Exception as e:
            self.summary_box.delete("1.0", tk.END)
            self.summary_box.insert(tk.END, f"❌ Error processing file: {e}")

    def copy_to_clipboard(self):
        try:
            text = self.summary_box.get("1.0", tk.END).strip()
            if text:
                self.frame.clipboard_clear()
                self.frame.clipboard_append(text)
                self.frame.update()
                messagebox.showinfo("Copied", "✅ Summary copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Clipboard Error", f"❌ Failed to copy: {e}")

    def export_summary(self):
        text = self.summary_box.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("No Content", "⚠️ No summary to save.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)
                messagebox.showinfo("Saved", f"✅ Summary saved to:\n{path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"❌ Failed to save: {e}")
