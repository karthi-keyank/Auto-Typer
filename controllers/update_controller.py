import threading
from tkinter import messagebox

import constants as C

from update_checker import check_for_update
from update_dialog import open_update_dialog


def check_for_updates(app, show_if_none: bool = False):
    """
    Checks for app updates in background.

    show_if_none:
        False -> silent (startup)
        True  -> show 'No updates available' (manual check)
    """

    def worker():
        try:
            result = check_for_update(
                current_version=C.APP_VERSION,
                owner=C.GITHUB_OWNER,
                repo=C.GITHUB_REPO
            )

            # ---------------------------------
            # UPDATE AVAILABLE
            # ---------------------------------
            if result:
                app.root.after(
                    0,
                    lambda: open_update_dialog(
                        parent=app.root,
                        current_version=C.APP_VERSION,
                        latest_version=result["latest_version"],
                        release_notes=result["release_notes"],
                        release_url=result["release_url"]
                    )
                )
                return

            # ---------------------------------
            # NO UPDATE (manual check only)
            # ---------------------------------
            if show_if_none:
                app.root.after(
                    0,
                    lambda: messagebox.showinfo(
                        "You're up to date",
                        f"You are using the latest version ({C.APP_VERSION})."
                    )
                )

        except Exception as e:
            # Silent on startup, visible on manual check
            if show_if_none:
                app.root.after(
                    0,
                    lambda: messagebox.showerror(
                        "Update check failed",
                        "Could not check for updates.\nPlease try again later."
                    )
                )
            else:
                print("Update check failed:", e)

    threading.Thread(target=worker, daemon=True).start()
