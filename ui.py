import tkinter as tk
from tkinter import ttk
import constants as C


def build_ui(app):
    root = app.root

    root.title(C.APP_TITLE)
    root.geometry(f"{C.WINDOW_WIDTH}x{C.WINDOW_HEIGHT}")

    # ✅ ENABLE RESIZING
    root.resizable(True, True)

    style = ttk.Style()
    style.theme_use(C.THEME)

    # Root grid config (IMPORTANT)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    main = ttk.Frame(root, padding=12)
    main.grid(row=0, column=0, sticky="nsew")

    # Main grid config
    main.columnconfigure(0, weight=1)
    main.rowconfigure(1, weight=1)  # text area grows

    # Title
    ttk.Label(
        main,
        text=C.APP_TITLE,
        font=C.FONT_TITLE
    ).grid(row=0, column=0, sticky="w", pady=(0, 6))

    # Text box (RESIZABLE CORE)
    app.text_box = tk.Text(
        main,
        font=C.FONT_TEXTBOX,
        wrap="word"
    )
    app.text_box.grid(row=1, column=0, sticky="nsew", pady=6)

    # Options row
    options = ttk.Frame(main)
    options.grid(row=2, column=0, sticky="w", pady=6)

    ttk.Label(options, text="Start Delay (sec):").grid(row=0, column=0)
    app.delay_entry = ttk.Entry(options, width=6)
    app.delay_entry.insert(0, C.DEFAULT_START_DELAY)
    app.delay_entry.grid(row=0, column=1, padx=5)

    ttk.Label(options, text="Character Delay (ms):").grid(row=0, column=2, padx=(15, 0))
    app.char_delay_entry = ttk.Entry(options, width=6)
    app.char_delay_entry.insert(0, C.DEFAULT_CHAR_DELAY)
    app.char_delay_entry.grid(row=0, column=3, padx=5)

    # Coding mode
    app.coding_mode = tk.BooleanVar(value=False)
    ttk.Checkbutton(
        options,
        text="Coding mode (auto delete paired brackets)",
        variable=app.coding_mode
    ).grid(row=0, column=4, padx=20)

    # Buttons row
    btns = ttk.Frame(main)
    btns.grid(row=3, column=0, pady=10)

    app.start_btn = ttk.Button(btns, text="Start", width=12, command=app.start)
    app.start_btn.grid(row=0, column=0, padx=6)

    app.pause_btn = ttk.Button(btns, text="Pause", width=12, command=app.pause)
    app.pause_btn.grid(row=0, column=1, padx=6)
    app.pause_btn.state(["disabled"])

    app.stop_btn = ttk.Button(btns, text="Stop", width=12, command=app.stop)
    app.stop_btn.grid(row=0, column=2, padx=6)
    app.stop_btn.state(["disabled"])

    app.restart_btn = ttk.Button(btns, text="Restart", width=12, command=app.restart)
    app.restart_btn.grid(row=0, column=3, padx=6)

    # Status bar (fixed height, full width)
    app.status_var = tk.StringVar(value=C.STATUS_KEYS)
    ttk.Label(
        main,
        textvariable=app.status_var,
        relief="sunken",
        anchor="w"
    ).grid(row=4, column=0, sticky="ew", pady=(8, 0))
