import threading
from tkinter import messagebox

from ui import build_ui
from typer import type_text
from hotkeys import bind_hotkeys
import constants as C


class AutoTyperApp:
    def __init__(self, root):
        self.root = root

        self.stop_event = threading.Event()
        self.resume_event = threading.Event()
        self.resume_event.set()

        self.is_running = False
        self.typed_count = 0

        build_ui(self)
        bind_hotkeys(self)

        self.update_progress()

    def start(self):
        if self.is_running:
            return

        text = self.text_box.get("1.0", "end").rstrip()
        if not text:
            self.status_var.set(C.STATUS_EMPTY)
            return

        try:
            delay = float(self.delay_entry.get())
            char_delay = float(self.char_delay_entry.get())
            if delay < 0 or char_delay < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid input", "Delays must be ≥ 0")
            return

        self.is_running = True
        self.stop_event.clear()
        self.resume_event.set()
        self.typed_count = 0

        self.start_btn.state(["disabled"])
        self.pause_btn.state(["!disabled"])
        self.stop_btn.state(["!disabled"])

        self.status_var.set(C.STATUS_WAITING)

        threading.Thread(
            target=type_text,
            args=(self, text, delay, char_delay),
            daemon=True
        ).start()

    def pause(self):
        if self.resume_event.is_set():
            self.resume_event.clear()
            self.pause_btn.config(text="Resume")
        else:
            self.resume_event.set()
            self.pause_btn.config(text="Pause")

    def stop(self):
        self.stop_event.set()
        self.resume_event.set()

    def restart(self):
        self.stop()
        self.start()

    def reset_ui(self, msg):
        self.is_running = False
        self.start_btn.state(["!disabled"])
        self.pause_btn.state(["disabled"])
        self.stop_btn.state(["disabled"])
        self.pause_btn.config(text="Pause")
        self.status_var.set(msg)

    def update_progress(self):
        self.root.after(C.PROGRESS_UPDATE_INTERVAL, self.update_progress)
