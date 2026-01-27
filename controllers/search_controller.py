from tkinter import messagebox
from file_cache import search_files, load_text_file


# ==================================================
# SEARCH (live)
# ==================================================
def on_search(app):
    query = app.search_var.get()
    results = search_files(query)

    app.search_results.delete(0, "end")

    if not results:
        app.search_results.grid_remove()
        return

    for r in results:
        app.search_results.insert("end", r["filename"])

    app.search_results.grid()


# ==================================================
# LISTBOX SELECT (mouse)
# ==================================================
def on_result_select(app):
    if not app.search_results.curselection():
        return
    load_selected_search_result(app)


# ==================================================
# LOAD SELECTED FILE (core logic)
# ==================================================
def load_selected_search_result(app):
    sel = app.search_results.curselection()
    if not sel:
        return

    index = sel[0]
    filename = app.search_results.get(index)

    try:
        content = load_text_file(filename)

        app.text_box.delete("1.0", "end")
        app.text_box.insert("1.0", content)

        # UX cleanup
        app.search_results.grid_remove()
        app.search_var.set("")
        app.text_box.focus_set()

        app.status_var.set(f"Loaded: {filename}")

    except Exception as e:
        messagebox.showerror("Load failed", str(e))
