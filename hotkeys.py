import tkinter as tk


def bind_search_hotkeys(app):
    entry = app.search_entry
    listbox = app.search_results

    # --------------------------------------------
    # Helpers
    # --------------------------------------------
    def list_visible():
        return listbox.winfo_ismapped()

    def list_size():
        return listbox.size()

    def select_index(index):
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(index)
        listbox.activate(index)
        listbox.see(index)

    # --------------------------------------------
    # ENTRY KEY HANDLERS
    # --------------------------------------------
    def entry_down(event):
        if not list_visible() or list_size() == 0:
            return "break"
        listbox.focus_set()
        select_index(0)
        return "break"

    def entry_enter(event):
        if list_visible() and list_size() > 0:
            listbox.focus_set()
            select_index(0)
            app.load_selected_search_result()   # ✅ SAFE
            return "break"

    def entry_escape(event):
        listbox.grid_remove()
        entry.focus_set()
        return "break"

    # --------------------------------------------
    # LISTBOX KEY HANDLERS
    # --------------------------------------------
    def list_up(event):
        if list_size() == 0:
            return "break"
        cur = listbox.curselection()
        index = cur[0] if cur else 0
        select_index(max(index - 1, 0))
        return "break"

    def list_down(event):
        if list_size() == 0:
            return "break"
        cur = listbox.curselection()
        index = cur[0] if cur else -1
        select_index(min(index + 1, list_size() - 1))
        return "break"

    def list_enter(event):
        if list_size() == 0:
            return "break"
        app.load_selected_search_result()      # ✅ SAFE
        return "break"

    def list_escape(event):
        listbox.grid_remove()
        entry.focus_set()
        return "break"

    # --------------------------------------------
    # Bindings
    # --------------------------------------------
    entry.bind("<Down>", entry_down)
    entry.bind("<Return>", entry_enter)
    entry.bind("<Escape>", entry_escape)

    listbox.bind("<Up>", list_up)
    listbox.bind("<Down>", list_down)
    listbox.bind("<Return>", list_enter)
    listbox.bind("<Escape>", list_escape)
