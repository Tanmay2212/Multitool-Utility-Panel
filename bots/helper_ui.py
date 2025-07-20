import tkinter as tk
import json

class HelperUI:
    def __init__(self, root, parent_frame):
        frame = tk.Frame(parent_frame, bg="#f8f9fa", padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="🧭 Tool Guide", font=("Segoe UI", 16, "bold"), bg="#f8f9fa").pack(anchor="w", pady=(0, 15))

        try:
            with open("config.json", "r") as f:
                tools = json.load(f)

            for tool in tools:
                name = f"🔧 {tool['name']}"
                desc = tool.get("description", "No description provided.")

                tk.Label(frame, text=name, font=("Segoe UI", 13, "bold"), bg="#f8f9fa", fg="#2d3436", anchor="w").pack(anchor="w", pady=(10, 2))
                tk.Label(frame, text=desc, font=("Segoe UI", 11), bg="#f8f9fa", wraplength=800, justify="left", fg="#636e72").pack(anchor="w")
        except Exception as e:
            tk.Label(frame, text=f"❌ Failed to load help: {e}", fg="red", bg="#f8f9fa").pack(anchor="w")
