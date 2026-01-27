import tkinter as tk
from tkinter import ttk
import webbrowser


def open_update_dialog(
    parent,
    current_version: str,
    latest_version: str,
    release_notes: str,
    release_url: str
):
    win = tk.Toplevel(parent)
    win.title("Update Available")
    win.geometry("720x600")
    win.minsize(600, 400)
    win.transient(parent)
    win.grab_set()

    # --------------------------------------------------
    # ROOT GRID
    # --------------------------------------------------
    win.columnconfigure(0, weight=1)
    win.rowconfigure(0, weight=1)

    main = ttk.Frame(win, padding=16)
    main.grid(row=0, column=0, sticky="nsew")
    main.columnconfigure(0, weight=1)

    # Row layout:
    # 0 = header (fixed)
    # 1 = spacer
    # 2 = notes (expand)
    # 3 = buttons (fixed)
    main.rowconfigure(2, weight=1)
    main.rowconfigure(3, weight=0)

    # --------------------------------------------------
    # HEADER
    # --------------------------------------------------
    header = ttk.Frame(main)
    header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
    header.columnconfigure(0, weight=1)

    ttk.Label(
        header,
        text="🔔 Update Available",
        font=("Segoe UI", 14, "bold")
    ).grid(row=0, column=0, sticky="w")

    ttk.Label(
        header,
        text=f"Current version: {current_version}    →    Latest version: {latest_version}",
        font=("Segoe UI", 9)
    ).grid(row=1, column=0, sticky="w", pady=(4, 0))

    # --------------------------------------------------
    # RELEASE NOTES
    # --------------------------------------------------
    notes_frame = ttk.LabelFrame(main, text=" Release Notes ")
    notes_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 12))
    notes_frame.columnconfigure(0, weight=1)
    notes_frame.rowconfigure(0, weight=1)

    text = tk.Text(
        notes_frame,
        wrap="word",
        font=("Consolas", 10),
        relief="flat",
        padx=8,
        pady=8
    )
    text.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(
        notes_frame,
        orient="vertical",
        command=text.yview
    )
    scrollbar.grid(row=0, column=1, sticky="ns")

    text.configure(yscrollcommand=scrollbar.set)

    text.insert("1.0", release_notes.strip() if release_notes else "No release notes provided.")
    text.config(state="disabled")

    # --------------------------------------------------
    # ACTION BUTTONS (ALWAYS VISIBLE)
    # --------------------------------------------------
    btns = ttk.Frame(main)
    btns.grid(row=3, column=0, sticky="se", pady=(0, 4))

    def on_download():
        webbrowser.open(release_url)
        win.destroy()

    def on_later():
        win.destroy()

    ttk.Button(
        btns,
        text="Download",
        width=12,
        command=on_download
    ).grid(row=0, column=0, padx=(0, 8))

    ttk.Button(
        btns,
        text="Later",
        width=10,
        command=on_later
    ).grid(row=0, column=1)

    # --------------------------------------------------
    # CLOSE HANDLING
    # --------------------------------------------------
    win.bind("<Escape>", lambda e: win.destroy())
    win.focus_set()
