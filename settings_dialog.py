import tkinter as tk
from tkinter import ttk, messagebox


def open_settings_dialog(parent, on_clear_cache, on_logout):
    win = tk.Toplevel(parent)
    win.title("Settings")
    win.resizable(False, False)
    win.transient(parent)
    win.grab_set()

    frame = ttk.Frame(win, padding=15)
    frame.grid()

    ttk.Label(frame, text="Settings", font=("Segoe UI", 12, "bold")).grid(
        row=0, column=0, sticky="w", pady=(0, 10)
    )

    def clear_cache():
        if messagebox.askyesno(
            "Clear Local Cache",
            "This will remove all locally saved texts.\nGoogle Drive will NOT be affected.\n\nContinue?"
        ):
            on_clear_cache()
            win.destroy()

    def logout():
        if messagebox.askyesno(
            "Logout",
            "You will be logged out from Google.\nYou will need to login again next time.\n\nContinue?"
        ):
            on_logout()
            win.destroy()

    ttk.Button(frame, text="🧹 Clear Local Cache", command=clear_cache).grid(
        row=1, column=0, sticky="ew", pady=5
    )

    ttk.Button(frame, text="🔐 Logout from Google", command=logout).grid(
        row=2, column=0, sticky="ew", pady=5
    )

    ttk.Button(frame, text="Close", command=win.destroy).grid(
        row=3, column=0, pady=(10, 0)
    )
