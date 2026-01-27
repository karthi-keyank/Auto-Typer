import threading
from tkinter import messagebox

import constants as C
from typer import type_text


# ==================================================
# START
# ==================================================
def start_typing(app):
    if app.is_running:
        return

    text = app.text_box.get("1.0", "end").rstrip()
    if not text:
        app.status_var.set(C.STATUS_EMPTY)
        return

    try:
        delay = float(app.delay_entry.get())
        char_delay = float(app.char_delay_entry.get())
        if delay < 0 or char_delay < 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning(
            "Invalid input",
            "Delays must be ≥ 0"
        )
        return

    app.is_running = True
    app.stop_event.clear()
    app.resume_event.set()
    app.typed_count = 0

    app.start_btn.state(["disabled"])
    app.pause_btn.state(["!disabled"])
    app.stop_btn.state(["!disabled"])

    app.status_var.set(C.STATUS_WAITING)

    threading.Thread(
        target=type_text,
        args=(app, text, delay, char_delay),
        daemon=True
    ).start()


# ==================================================
# PAUSE / RESUME
# ==================================================
def pause_typing(app):
    if not app.is_running:
        return

    if app.resume_event.is_set():
        app.resume_event.clear()
        app.pause_btn.config(text="Resume")
        app.status_var.set(C.STATUS_PAUSED)
    else:
        app.resume_event.set()
        app.pause_btn.config(text="Pause")
        app.status_var.set(C.STATUS_TYPING)


# ==================================================
# STOP
# ==================================================
def stop_typing(app):
    if not app.is_running:
        return
    app.stop_event.set()
    app.resume_event.set()


# ==================================================
# RESTART
# ==================================================
def restart_typing(app):
    stop_typing(app)
    start_typing(app)


# ==================================================
# RESET UI (called by typer.py)
# ==================================================
def reset_ui(app, msg):
    app.is_running = False

    app.start_btn.state(["!disabled"])
    app.pause_btn.state(["disabled"])
    app.stop_btn.state(["disabled"])

    app.pause_btn.config(text="Pause")
    app.status_var.set(msg)

    # reset progress safely
    if hasattr(app, "progress_var"):
        app.progress_var.set(0)


# ==================================================
# PROGRESS LOOP (DEFENSIVE)
# ==================================================
def update_progress(app):
    if (
        app.is_running
        and hasattr(app, "progress_var")
        and hasattr(app, "progress_max")
    ):
        value = min(app.typed_count, app.progress_max)
        app.progress_var.set(value)

    app.root.after(
        C.PROGRESS_UPDATE_INTERVAL,
        lambda: update_progress(app)
    )
