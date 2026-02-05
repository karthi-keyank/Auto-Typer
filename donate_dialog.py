import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def center_window(win):
    win.update_idletasks()
    w = win.winfo_width()
    h = win.winfo_height()

    x = (win.winfo_screenwidth() // 2) - (w // 2)
    y = (win.winfo_screenheight() // 2) - (h // 2)

    win.geometry(f"+{x}+{y}")


def open_donate_dialog(parent, exit_after=True):
    win = tk.Toplevel(parent)
    win.title("Support Auto Typer ❤️")
    win.resizable(False, False)
    win.transient(parent)
    win.grab_set()

    frame = ttk.Frame(win, padding=26)
    frame.pack(fill="both", expand=True)

    # ---------- TITLE ----------
    ttk.Label(
        frame,
        text="Support Auto Typer ❤️",
        font=("Segoe UI", 15, "bold")
    ).pack(pady=(0, 10))

    ttk.Label(
        frame,
        text=(
            "If this app helped you even a little,\n"
            "consider donating.\n\n"
            "Your support helps improve features,\n"
            "servers, and future updates."
        ),
        justify="center",
        wraplength=380
    ).pack(pady=(0, 18))

    content = ttk.Frame(frame)
    content.pack(fill="x")

    # ---------- UPI VIEW ----------
    upi_view = ttk.Frame(content, padding=14, relief="ridge")

    upi_id = "karthikeyan02116k-1@okicici"

    ttk.Label(
        upi_view,
        text="UPI ID",
        font=("Segoe UI", 9, "bold")
    ).pack(anchor="w")

    row = ttk.Frame(upi_view)
    row.pack(fill="x", pady=(6, 0))

    ttk.Label(
        row,
        text=upi_id,
        font=("Consolas", 12)
    ).pack(side="left")

    def copy_upi():
        parent.clipboard_clear()
        parent.clipboard_append(upi_id)
        messagebox.showinfo("Copied", "UPI ID copied to clipboard ❤️")

    ttk.Button(
        row,
        text="📋 Copy",
        command=copy_upi
    ).pack(side="right")

    # ---------- QR VIEW ----------
    qr_view = ttk.Frame(content, padding=14)

    qr_label = ttk.Label(qr_view)
    qr_label.pack()

    qr_loaded = False

    def load_qr():
        nonlocal qr_loaded
        if qr_loaded:
            return

        path = resource_path("assets/gpay_qr.png")
        if not os.path.exists(path):
            messagebox.showerror("Error", "QR image not found")
            return

        img = tk.PhotoImage(file=path)

        img = img.subsample(5, 6)

        qr_label.configure(image=img)
        qr_label.image = img
        qr_loaded = True

    # ---------- TOGGLE ----------
    showing_qr = False

    def toggle_view():
        nonlocal showing_qr

        if showing_qr:
            qr_view.pack_forget()
            upi_view.pack(fill="x")
            toggle_btn.config(text="Show QR Code")
            showing_qr = False
        else:
            upi_view.pack_forget()
            load_qr()
            qr_view.pack()
            toggle_btn.config(text="Show UPI ID")
            showing_qr = True

    upi_view.pack(fill="x")

    toggle_btn = ttk.Button(
        frame,
        text="Show QR Code",
        command=toggle_view
    )
    toggle_btn.pack(pady=14)

    # ---------- ACTION BUTTONS ----------
    btns = ttk.Frame(frame)
    btns.pack(pady=(10, 0))

    def close_all():
        win.destroy()
        if exit_after:
            parent.destroy()
            sys.exit(0)

    ttk.Button(
        btns,
        text="❤️ Donated!",
        width=15,
        command=close_all
    ).pack(side="left", padx=8)

    ttk.Button(
        btns,
        text="😔 Sorry",
        width=15,
        command=close_all
    ).pack(side="right", padx=8)

    center_window(win)
