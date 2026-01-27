import threading
from tkinter import Tk

from ui import build_ui

# Controllers
from controllers.typing_controller import (
    start_typing,
    pause_typing,
    stop_typing,
    restart_typing,
    update_progress
)

from controllers.cloud_controller import (
    auto_fetch_on_start,
    fetch_texts,
    upload_text
)

from controllers.search_controller import (
    on_search,
    on_result_select,
    load_selected_search_result
)

from controllers.settings_controller import open_settings
from controllers.update_controller import check_for_updates   # 👈 NEW


class AutoTyperApp:
    def __init__(self, root: Tk):
        self.root = root

        # ---------------------------------
        # Runtime state
        # ---------------------------------
        self.is_running = False
        self.typed_count = 0

        self.stop_event = threading.Event()
        self.resume_event = threading.Event()
        self.resume_event.set()

        self.backend = None

        # ---------------------------------
        # UI
        # ---------------------------------
        build_ui(self)

        # ---------------------------------
        # Search bindings
        # ---------------------------------
        self.search_var.trace_add(
            "write",
            lambda *args: on_search(self)
        )

        self.search_results.bind(
            "<<ListboxSelect>>",
            lambda event: on_result_select(self)
        )

        # ---------------------------------
        # Startup tasks (non-blocking)
        # ---------------------------------
        self.root.after(500, lambda: auto_fetch_on_start(self))
        self.root.after(800, lambda: check_for_updates(self))   # 👈 UPDATE CHECK

        update_progress(self)

    # ==================================================
    # Button bridges
    # ==================================================
    def start(self): start_typing(self)
    def pause(self): pause_typing(self)
    def stop(self): stop_typing(self)
    def restart(self): restart_typing(self)
    def fetch(self): fetch_texts(self)
    def upload(self): upload_text(self)
    def open_settings(self): open_settings(self)

    # ==================================================
    # 🔑 SEARCH BRIDGE
    # ==================================================
    def load_selected_search_result(self):
        load_selected_search_result(self)
