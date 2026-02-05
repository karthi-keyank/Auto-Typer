from file_cache import clear_cache
from controllers.update_controller import check_for_updates
from settings_dialog import open_settings_dialog
from donate_dialog import open_donate_dialog


# ==================================================
# SETTINGS
# ==================================================
def open_settings(app):

    def do_clear_cache():
        clear_cache()

        app.search_results.delete(0, "end")
        app.search_results.grid_remove()
        app.text_box.delete("1.0", "end")

        app.status_var.set("Local cache cleared")

    def do_reset_backend():
        app.backend = None
        app.status_var.set("Cloud connection reset")

    def do_check_updates():
        app.status_var.set("Checking for updates…")
        check_for_updates(app, show_if_none=True)

    def do_donate():
        open_donate_dialog(app.root, exit_after=False)

    open_settings_dialog(
        parent=app.root,
        on_clear_cache=do_clear_cache,
        on_logout=do_reset_backend,
        on_check_updates=do_check_updates,  # ✅ comma added
        on_donate=do_donate
    )
