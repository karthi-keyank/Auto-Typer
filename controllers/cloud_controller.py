import threading
from tkinter import messagebox

from firebase_client import FirebaseClient
from file_cache import save_text_file


# ==================================================
# INTERNAL: ENSURE BACKEND
# ==================================================
def _ensure_backend(app):
    if app.backend is None:
        app.root.after(
            0,
            lambda: app.status_var.set("Connecting to cloud…")
        )
        app.backend = FirebaseClient()


# ==================================================
# AUTO FETCH ON STARTUP
# ==================================================
def auto_fetch_on_start(app):
    def worker():
        try:
            app.root.after(
                0,
                lambda: app.status_var.set("Auto fetching texts…")
            )

            _ensure_backend(app)
            files = app.backend.list_text_files()

            for f in files:
                content = app.backend.download_text(f["id"])
                save_text_file(f["name"], content)

            app.root.after(
                0,
                lambda: app.status_var.set(f"Auto fetched {len(files)} files")
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
            _ensure_backend(app)
            app.root.after(
                0,
                lambda: app.status_var.set("Fetching texts…")
            )

            files = app.backend.list_text_files()

            for f in files:
                content = app.backend.download_text(f["id"])
                save_text_file(f["name"], content)

            app.root.after(
                0,
                lambda: app.status_var.set(f"Fetched {len(files)} files")
            )

        except Exception as e:
            app.root.after(
                0,
                lambda: messagebox.showerror("Fetch failed", str(e))
            )
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
            _ensure_backend(app)
            app.root.after(
                0,
                lambda: app.status_var.set("Uploading…")
            )

            final_name = app.backend.upload_text(filename, text)

            app.root.after(
                0,
                lambda: app.status_var.set(f"Uploaded: {final_name}")
            )

        except Exception as e:
            app.root.after(
                0,
                lambda: messagebox.showerror("Upload failed", str(e))
            )
            app.root.after(
                0,
                lambda: app.status_var.set("Upload failed")
            )

    threading.Thread(target=worker, daemon=True).start()
