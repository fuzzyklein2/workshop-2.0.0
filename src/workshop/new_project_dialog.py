#!/usr/bin/env python3
from pathlib import Path
import subprocess
import tkinter as tk
from tkinter import ttk
from pygnition._git_tools import get_github_username
from pygnition.tools import cwd
from .constants import COMMON_LICENSES, KEY_PROMPTS
from pygnition.lumberjack import debug

def new_project_dialog(key_prompts):
    root = tk.Tk()
    root.title("Project Information")
    root.minsize(560, 260)

    for c in range(4):
        root.columnconfigure(c, weight=1 if c in (1,3) else 0)

    entries = {}
    result = {}

    # Get author and GitHub username
    try:
        author = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True).stdout.strip()
        if not author:
            from pygnition import get_full_name
            author = get_full_name()
    except Exception:
        from pygnition import get_full_name
        author = get_full_name()
    github_user = get_github_username() or "<user>"
    debug(f'{github_user=}')

    # Row 0: Name + Version
    row = 0
    tk.Label(root, text="Project Name:").grid(row=row, column=0, sticky="w", padx=5, pady=3)
    name_entry = ttk.Entry(root)
    name_entry.grid(row=row, column=1, sticky="ew", padx=5, pady=3)
    entries["name"] = name_entry

    tk.Label(root, text="Version:").grid(row=row, column=2, sticky="w", padx=5, pady=3)
    version_entry = ttk.Entry(root)
    version_entry.grid(row=row, column=3, sticky="ew", padx=5, pady=3)
    entries["version"] = version_entry

    # Row 1: Path
    row += 1
    tk.Label(root, text="Path:").grid(row=row, column=0, sticky="w", padx=5, pady=3)
    path_entry = ttk.Entry(root)
    path_entry.grid(row=row, column=1, columnspan=3, sticky="ew", padx=5, pady=3)
    entries["path"] = path_entry

    # Row 2: Project Type + Author
    row += 1
    tk.Label(root, text="Project Type:").grid(row=row, column=0, sticky="w", padx=5, pady=3)
    type_labels = ["Script","Module","Package","Program","Filter","Driver","CGI","TK","GTK","Webkit"]
    type_map = {v:v.lower() for v in type_labels}
    type_var = tk.StringVar(value="Script")
    type_cb = ttk.Combobox(root, textvariable=type_var, values=type_labels, state="readonly", width=20)
    type_cb.grid(row=row, column=1, sticky="ew", padx=5, pady=3)
    entries["type"] = type_var

    tk.Label(root, text="Author:").grid(row=row, column=2, sticky="w", padx=5, pady=3)
    author_entry = ttk.Entry(root)
    author_entry.grid(row=row, column=3, sticky="ew", padx=5, pady=3)
    entries["author"] = author_entry
    if author:
        author_entry.insert(0, author)

    # Remaining fields
    for key, prompt in key_prompts:
        if key in ("name","version","path","type","author"):
            continue
        row += 1
        tk.Label(root, text=prompt).grid(row=row, column=0, sticky="w", padx=5, pady=3)
        if key == "license":
            val = tk.StringVar(value="MIT")
            cb = ttk.Combobox(root, textvariable=val, values=COMMON_LICENSES, state="readonly", width=25)
            cb.grid(row=row, column=1, sticky="ew", padx=5, pady=3)
            entries[key] = val
            vis_var = tk.StringVar(value="public")
            ttk.Radiobutton(root, text="Public", variable=vis_var, value="public").grid(row=row,column=2,sticky="w",padx=5)
            ttk.Radiobutton(root, text="Private", variable=vis_var, value="private").grid(row=row,column=3,sticky="w",padx=5)
            entries["visibility"] = vis_var
        else:
            entry = ttk.Entry(root)
            entry.grid(row=row, column=1, columnspan=3, sticky="ew", padx=5, pady=3)
            entries[key] = entry

    # GitHub field
    gh_entry = entries.get("github")

    def update_path_and_github(*_):
        name = name_entry.get().strip() or "<name>"
        version = version_entry.get().strip() or "<version>"
        path_entry.delete(0, tk.END)
        path_entry.insert(0, str(cwd()/f"{name}-{version}"))
        path_entry.config(foreground="gray" if "<name>" in name or "<version>" in version else "black")
        if gh_entry:
            gh_url = f"https://github.com/{github_user}/{name}-{version}.git"
            gh_entry.delete(0, tk.END)
            gh_entry.insert(0, gh_url)
            gh_entry.config(foreground="gray" if "<name>" in name or "<version>" in version else "black")

    name_entry.bind("<KeyRelease>", update_path_and_github, add="+")
    version_entry.bind("<KeyRelease>", update_path_and_github, add="+")
    update_path_and_github()

    # Buttons
    def on_ok(event=None):
        for k,w in entries.items():
            if isinstance(w, ttk.Entry):
                result[k] = w.get().strip()
            elif isinstance(w, tk.StringVar):
                result[k] = w.get().strip()
        root.destroy()

    def on_cancel(event=None):
        result.clear()
        root.destroy()

    row += 1
    btn_frame = ttk.Frame(root)
    btn_frame.grid(row=row,column=0,columnspan=4,pady=10,sticky="e")
    ttk.Button(btn_frame,text="Cancel",command=on_cancel).pack(side="right",padx=(0,6))
    ttk.Button(btn_frame,text="OK",command=on_ok).pack(side="right")
    root.bind("<Return>", on_ok)
    root.bind("<Escape>", on_cancel)

    root.update_idletasks()
    w,h = root.winfo_width(), root.winfo_height()
    sw,sh = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry(f"+{(sw-w)//2}+{(sh-h)//2}")
    name_entry.focus_set()
    root.lift()
    root.attributes("-topmost",True)
    root.after(200, lambda: root.attributes("-topmost",False))
    root.mainloop()
    return result

if __name__ == "__main__":
    KEY_PROMPTS = [
        ('name','Project Name:'),
        ('version','Version:'),
        ('author','Author:'),
        ('type','Project Type:'),
        ('description','Description:'),
        ('requirements','Requirements:'),
        ('github','GitHub Repository:'),
        ('license','License:')
    ]
    data = new_project_dialog(KEY_PROMPTS)
    print("Collected:", data)
