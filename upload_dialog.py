import tkinter as tk
from tkinter import ttk, messagebox


MAX_TAGS = 3


class UploadDialog:
    def __init__(self, parent):
        self.result = None

        self.window = tk.Toplevel(parent)
        self.window.title("Upload Text")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        self._build_ui()

        self.window.wait_window()

    # --------------------------------------------------
    # UI
    # --------------------------------------------------
    def _build_ui(self):
        frame = ttk.Frame(self.window, padding=12)
        frame.grid(row=0, column=0)

        ttk.Label(
            frame,
            text="Enter name and tags",
            font=("Segoe UI", 11, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        ttk.Label(
            frame,
            text="Example: sorting notes #dsa #algo"
        ).grid(row=1, column=0, sticky="w")

        self.entry = ttk.Entry(frame, width=40)
        self.entry.grid(row=2, column=0, pady=8)
        self.entry.focus()

        btns = ttk.Frame(frame)
        btns.grid(row=3, column=0, pady=(8, 0))

        ttk.Button(btns, text="OK", command=self._on_ok).grid(row=0, column=0, padx=6)
        ttk.Button(btns, text="Cancel", command=self._on_cancel).grid(row=0, column=1, padx=6)

    # --------------------------------------------------
    # LOGIC
    # --------------------------------------------------
    def _on_ok(self):
        text = self.entry.get().strip()

        if not text:
            messagebox.showwarning("Invalid input", "Name cannot be empty")
            return

        parts = text.split()
        tags = [p for p in parts if p.startswith("#")]

        if len(tags) > MAX_TAGS:
            messagebox.showwarning(
                "Too many tags",
                f"Maximum {MAX_TAGS} tags allowed"
            )
            return

        filename = f"{text}.txt"
        self.result = filename
        self.window.destroy()

    def _on_cancel(self):
        self.result = None
        self.window.destroy()


# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------
def ask_upload_filename(parent):
    dialog = UploadDialog(parent)
    return dialog.result
