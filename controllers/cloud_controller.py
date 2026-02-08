import threading
from tkinter import messagebox

from firebase_client import FirebaseClient
from file_cache import (
    save_text_file,
    load_fetched_ids,
    save_fetched_ids
)

# ==================================================
# INTERNAL: ENSURE BACKEND (THREAD-SAFE)
# ==================================================

_backend_lock = threading.Lock()


def _ensure_backend(app):
    if app.backend is None:
        with _backend_lock:
            if app.backend is None:
                app.backend = FirebaseClient()


# ==================================================
# AUTO FETCH ON STARTUP  ✅ RESTORED
# ==================================================

def auto_fetch_on_start(app):
    def worker():
        try:
            app.root.after(
                0,
                lambda: app.status_var.set("Auto fetching new texts…")
            )

            _ensure_backend(app)

            fetched_ids = load_fetched_ids()
            files = app.backend.list_text_files()

            new_count = 0

            for f in files:
                if f["id"] in fetched_ids:
                    continue

                content = app.backend.download_text(f["id"])
                save_text_file(f["name"], content)

                fetched_ids.add(f["id"])
                new_count += 1

            save_fetched_ids(fetched_ids)

            app.root.after(
                0,
                lambda: app.status_var.set(
                    f"Auto fetched {new_count} new file(s)"
                )
            )

        except Exception as e:
            print("Auto fetch error:", e)
            app.root.after(
                0,
                lambda: app.status_var.set("Auto fetch failed")
            )

    threading.Thread(target=worker, daemon=True).start()


# ==================================================
# MANUAL FETCH
# ==================================================

def fetch_texts(app):
    def worker():
        try:
            app.root.after(
                0,
                lambda: app.status_var.set("Fetching new texts…")
            )

            _ensure_backend(app)

            fetched_ids = load_fetched_ids()
            files = app.backend.list_text_files()

            new_count = 0

            for f in files:
                if f["id"] in fetched_ids:
                    continue

                content = app.backend.download_text(f["id"])
                save_text_file(f["name"], content)

                fetched_ids.add(f["id"])
                new_count += 1

            save_fetched_ids(fetched_ids)

            app.root.after(
                0,
                lambda: app.status_var.set(
                    f"Fetched {new_count} new file(s)"
                )
            )

        except Exception as e:
            print("Fetch error:", e)
            app.root.after(
                0,
                lambda: app.status_var.set("Fetch failed")
            )

    threading.Thread(target=worker, daemon=True).start()


# ==================================================
# UPLOAD
# ==================================================

def upload_text(app):
    from upload_dialog import ask_upload_filename

    text = app.text_box.get("1.0", "end").rstrip()
    if not text:
        messagebox.showwarning("Nothing to upload", "Text box is empty")
        return

    filename = ask_upload_filename(app.root)
    if filename is None:
        return

    def worker():
        try:
            app.root.after(
                0,
                lambda: app.status_var.set("Uploading…")
            )

            _ensure_backend(app)

            final_name = app.backend.upload_text(filename, text)

            app.root.after(
                0,
                lambda: app.status_var.set(f"Uploaded: {final_name}")
            )

        except Exception as e:
            print("Upload error:", e)
            app.root.after(
                0,
                lambda: messagebox.showerror("Upload failed", str(e))
            )
            app.root.after(
                0,
                lambda: app.status_var.set("Upload failed")
            )

    threading.Thread(target=worker, daemon=True).start()
