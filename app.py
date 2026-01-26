import threading
from tkinter import messagebox

from ui import build_ui
from typer import type_text
import constants as C

from firebase_client import FirebaseClient
from settings_dialog import open_settings_dialog

from file_cache import (
    save_text_file,
    load_text_file,
    search_files,
    clear_cache
)

from upload_dialog import ask_upload_filename


class AutoTyperApp:
    def __init__(self, root):
        self.root = root

        # -------------------------------
        # Typing control
        # -------------------------------
        self.stop_event = threading.Event()
        self.resume_event = threading.Event()
        self.resume_event.set()

        self.is_running = False
        self.typed_count = 0

        # Firebase client (lazy init)
        self.backend = None

        # -------------------------------
        # UI
        # -------------------------------
        build_ui(self)

        # Search bindings
        self.search_var.trace_add("write", self.on_search)
        self.search_results.bind("<<ListboxSelect>>", self.on_result_select)

        # Auto fetch AFTER UI loads
        self.root.after(500, self.auto_fetch_on_start)

        self.update_progress()

    # ==================================================
    # TYPING LOGIC
    # ==================================================
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

    # ==================================================
    # BACKEND INIT (Firebase)
    # ==================================================
    def _ensure_backend(self):
        if self.backend is None:
            self.status_var.set("Connecting to cloud…")
            self.backend = FirebaseClient()

    # ==================================================
    # AUTO FETCH ON START
    # ==================================================
    def auto_fetch_on_start(self):
        def worker():
            try:
                self.status_var.set("Auto fetching texts…")
                self._ensure_backend()

                files = self.backend.list_text_files()
                for f in files:
                    content = self.backend.download_text(f["id"])
                    save_text_file(f["name"], content)

                self.status_var.set(f"Auto fetched {len(files)} files")

            except Exception as e:
                self.status_var.set("Auto fetch failed")
                print("Auto fetch error:", e)

        threading.Thread(target=worker, daemon=True).start()

    # ==================================================
    # UPLOAD
    # ==================================================
    def upload(self):
        text = self.text_box.get("1.0", "end").rstrip()
        if not text:
            messagebox.showwarning("Nothing to upload", "Text box is empty")
            return

        filename = ask_upload_filename(self.root)
        if filename is None:
            return

        def worker():
            try:
                self._ensure_backend()
                self.status_var.set("Uploading…")

                final_name = self.backend.upload_text(filename, text)
                self.status_var.set(f"Uploaded: {final_name}")

            except Exception as e:
                messagebox.showerror("Upload failed", str(e))
                self.status_var.set("Upload failed")

        threading.Thread(target=worker, daemon=True).start()

    # ==================================================
    # FETCH (MANUAL)
    # ==================================================
    def fetch(self):
        def worker():
            try:
                self._ensure_backend()
                self.status_var.set("Fetching texts…")

                files = self.backend.list_text_files()
                for f in files:
                    content = self.backend.download_text(f["id"])
                    save_text_file(f["name"], content)

                self.status_var.set(f"Fetched {len(files)} files")

            except Exception as e:
                messagebox.showerror("Fetch failed", str(e))
                self.status_var.set("Fetch failed")

        threading.Thread(target=worker, daemon=True).start()

    # ==================================================
    # SEARCH
    # ==================================================
    def on_search(self, *args):
        query = self.search_var.get()
        results = search_files(query)

        self.search_results.delete(0, "end")

        if not results:
            self.search_results.grid_remove()
            return

        for r in results:
            self.search_results.insert("end", r["filename"])

        self.search_results.grid()

    def on_result_select(self, event):
        if not self.search_results.curselection():
            return

        index = self.search_results.curselection()[0]
        filename = self.search_results.get(index)

        try:
            content = load_text_file(filename)
            self.text_box.delete("1.0", "end")
            self.text_box.insert("1.0", content)
            self.status_var.set(f"Loaded: {filename}")
        except Exception as e:
            messagebox.showerror("Load failed", str(e))

    # ==================================================
    # SETTINGS
    # ==================================================
    def open_settings(self):
        def do_clear_cache():
            clear_cache()
            self.search_results.delete(0, "end")
            self.search_results.grid_remove()
            self.text_box.delete("1.0", "end")
            self.status_var.set("Local cache cleared")

        def do_reset_backend():
            self.backend = None
            self.status_var.set("Cloud connection reset")

        open_settings_dialog(
            self.root,
            on_clear_cache=do_clear_cache,
            on_logout=do_reset_backend
        )
