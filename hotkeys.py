import constants as C


def bind_hotkeys(app):
    app.root.bind("r", lambda e: app.start())
    app.root.bind("p", lambda e: app.pause())
    app.root.bind("s", lambda e: app.stop())

    app.status_var.set(C.STATUS_KEYS)
