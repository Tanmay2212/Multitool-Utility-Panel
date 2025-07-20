import tkinter as tk

def show_selector_ui(root, matches, keyword):
    top = tk.Toplevel(root)
    top.title(f"Select matches for '{keyword}'")

    listbox = tk.Listbox(top, selectmode="multiple", width=80, height=20)
    listbox.pack(padx=10, pady=10)

    for i, m in enumerate(matches):
        preview = m["text"][:50]
        listbox.insert("end", f"Page {m['page']+1}: {preview}")

    selected = []

    def confirm():
        for i in listbox.curselection():
            selected.append(matches[i])
        top.destroy()

    tk.Button(top, text="✅ Confirm", command=confirm).pack(pady=10)
    top.grab_set()
    root.wait_window(top)
    return selected
