import tkinter as tk
from tkinter import ttk
from utils.logger import log_event
import importlib
import json

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Multitool Utility Panel 🚀")
        self.root.geometry("1100x720")
        self.root.configure(bg="#f0f0f0")

        self.active_button = None

        # Sidebar styling
        self.sidebar = tk.Frame(root, width=240, bg="#1f1f1f")
        self.sidebar.pack(side="left", fill="y")

        self.main = tk.Frame(root, bg="#ffffff")
        self.main.pack(side="right", expand=True, fill="both")

        # Header
        tk.Label(
            self.sidebar,
            text="⚙️ Tools Menu",
            bg="#1f1f1f",
            fg="white",
            font=("Segoe UI", 16, "bold"),
            pady=15
        ).pack()

        # Load tools from config.json
        with open("config.json", "r") as f:
            self.tools_config = json.load(f)

        self.buttons = []
        for tool in self.tools_config:
            btn = tk.Button(
                self.sidebar,
                text=f"🔧 {tool['name']}",
                command=lambda t=tool, b=len(self.buttons): self.load_tool(t, b),
                font=("Segoe UI", 11),
                bg="#2b2b2b", fg="white",
                activebackground="#3a3a3a",
                activeforeground="#00ffcc",
                bd=0,
                padx=10,
                pady=10,
                anchor="w"
            )
            btn.pack(fill="x", pady=2, padx=10)
            self.buttons.append(btn)

    def clear_main(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def highlight_button(self, index):
        for i, btn in enumerate(self.buttons):
            if i == index:
                btn.configure(bg="#00b894", fg="black")
            else:
                btn.configure(bg="#2b2b2b", fg="white")

    def load_tool(self, tool, index):
        try:
            self.clear_main()
            self.highlight_button(index)
            module = importlib.import_module(tool["module"])
            tool_class = getattr(module, tool["class"])
            tool_class(self.root, self.main)  # Load into main panel
            log_event("Navigation", f"Opened {tool['name']}")
        except Exception as e:
            print(f"❌ Failed to load {tool['name']}: {e}")
            log_event("Error", f"Failed to load {tool['name']}: {e}")
            tk.Label(self.main, text=f"❌ Error loading tool:\n{e}", fg="red", bg="white", font=("Arial", 12)).pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
