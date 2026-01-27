import tkinter as tk
from tkinter import ttk, messagebox


def open_settings_dialog(
    parent,
    on_clear_cache,
    on_logout,
    on_check_updates        # 👈 NEW
):
    win = tk.Toplevel(parent)
    win.title("Settings")
    win.resizable(False, False)
    win.transient(parent)
    win.grab_set()

    frame = ttk.Frame(win, padding=15)
    frame.grid()

    ttk.Label(
        frame,
        text="Settings",
        font=("Segoe UI", 12, "bold")
    ).grid(row=0, column=0, sticky="w", pady=(0, 10))

    # --------------------------------------------------
    # CLEAR CACHE
    # --------------------------------------------------
    def clear_cache():
        if messagebox.askyesno(
            "Clear Local Cache",
            "This will remove all locally saved texts.\n"
            "Cloud data will NOT be affected.\n\n"
            "Continue?"
        ):
            on_clear_cache()
            win.destroy()

    # --------------------------------------------------
    # RESET CLOUD CONNECTION
    # --------------------------------------------------
    def reset_cloud():
        if messagebox.askyesno(
            "Reset Cloud Connection",
            "This will reset the cloud connection.\n"
            "No data will be deleted.\n\n"
            "Continue?"
        ):
            on_logout()
            win.destroy()

    # --------------------------------------------------
    # CHECK FOR UPDATES
    # --------------------------------------------------
    def check_updates():
        on_check_updates()
        win.destroy()

    ttk.Button(
        frame,
        text="🧹 Clear Local Cache",
        command=clear_cache
    ).grid(row=1, column=0, sticky="ew", pady=5)

    ttk.Button(
        frame,
        text="☁ Reset Cloud Connection",
        command=reset_cloud
    ).grid(row=2, column=0, sticky="ew", pady=5)

    ttk.Button(
        frame,
        text="🔄 Check for Updates",     # 👈 NEW
        command=check_updates
    ).grid(row=3, column=0, sticky="ew", pady=5)

    ttk.Button(
        frame,
        text="Close",
        command=win.destroy
    ).grid(row=4, column=0, pady=(10, 0))
