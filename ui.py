import tkinter as tk
from tkinter import ttk
import constants as C

# 🔑 keyboard bindings live here
from hotkeys import bind_search_hotkeys


def build_ui(app):
    root = app.root

    # --------------------------------------------------
    # WINDOW
    # --------------------------------------------------
    root.title(C.APP_TITLE)
    root.geometry(f"{C.WINDOW_WIDTH}x{C.WINDOW_HEIGHT}")
    root.resizable(True, True)

    style = ttk.Style()
    style.theme_use(C.THEME)

    # --------------------------------------------------
    # ROOT GRID
    # --------------------------------------------------
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    main = ttk.Frame(root, padding=14)
    main.grid(row=0, column=0, sticky="nsew")

    main.columnconfigure(0, weight=1)
    main.rowconfigure(3, weight=1)

    # --------------------------------------------------
    # HEADER
    # --------------------------------------------------
    header = ttk.Frame(main)
    header.grid(row=0, column=0, sticky="ew", pady=(0, 8))
    header.columnconfigure(0, weight=1)

    ttk.Label(
        header,
        text=C.APP_TITLE,
        font=C.FONT_TITLE
    ).grid(row=0, column=0, sticky="w")

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------
    search_frame = ttk.LabelFrame(main, text=" Search ")
    search_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
    search_frame.columnconfigure(1, weight=1)

    ttk.Label(search_frame, text="🔍").grid(row=0, column=0, padx=(6, 4))

    app.search_var = tk.StringVar()

    app.search_entry = ttk.Entry(
        search_frame,
        textvariable=app.search_var
    )
    app.search_entry.grid(
        row=0,
        column=1,
        sticky="ew",
        padx=(0, 6),
        pady=4
    )

    # --------------------------------------------------
    # SEARCH RESULTS (DROPDOWN)
    # --------------------------------------------------
    app.search_results = tk.Listbox(
        main,
        height=6,
        activestyle="dotbox",
        exportselection=False
    )
    app.search_results.grid(
        row=2,
        column=0,
        sticky="ew",
        pady=(0, 6)
    )
    app.search_results.grid_remove()

    # 🔑 keyboard UX bindings
    bind_search_hotkeys(app)

    # --------------------------------------------------
    # TEXT EDITOR
    # --------------------------------------------------
    editor_frame = ttk.LabelFrame(main, text=" Text to Type ")
    editor_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 8))
    editor_frame.columnconfigure(0, weight=1)
    editor_frame.rowconfigure(0, weight=1)

    app.text_box = tk.Text(
        editor_frame,
        font=C.FONT_TEXTBOX,
        wrap="word",
        undo=True
    )
    app.text_box.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=4,
        pady=4
    )

    # --------------------------------------------------
    # OPTIONS
    # --------------------------------------------------
    options = ttk.LabelFrame(main, text=" Options ")
    options.grid(row=4, column=0, sticky="ew", pady=(0, 8))

    ttk.Label(options, text="Start delay (sec):").grid(
        row=0, column=0, padx=6, pady=4
    )

    app.delay_entry = ttk.Entry(options, width=6)
    app.delay_entry.insert(0, C.DEFAULT_START_DELAY)
    app.delay_entry.grid(row=0, column=1, pady=4)

    ttk.Label(options, text="Char delay (ms):").grid(
        row=0, column=2, padx=(16, 6), pady=4
    )

    app.char_delay_entry = ttk.Entry(options, width=6)
    app.char_delay_entry.insert(0, C.DEFAULT_CHAR_DELAY)
    app.char_delay_entry.grid(row=0, column=3, pady=4)

    # ✅ Coding mode ON by default
    app.coding_mode = tk.BooleanVar(value=True)

    ttk.Checkbutton(
        options,
        text="Coding mode (auto delete paired brackets)",
        variable=app.coding_mode
    ).grid(row=0, column=4, padx=16, pady=4)

    # --------------------------------------------------
    # ACTION BUTTONS
    # --------------------------------------------------
    btns = ttk.Frame(main)
    btns.grid(row=5, column=0, pady=(4, 8))

    def add_btn(col, text, cmd):
        b = ttk.Button(btns, text=text, width=11, command=cmd)
        b.grid(row=0, column=col, padx=4)
        return b

    app.start_btn    = add_btn(0, "▶ Start", app.start)
    app.pause_btn    = add_btn(1, "⏸ Pause", app.pause)
    app.stop_btn     = add_btn(2, "⏹ Stop", app.stop)
    app.restart_btn  = add_btn(3, "🔁 Restart", app.restart)
    app.upload_btn   = add_btn(4, "⬆ Upload", app.upload)
    app.fetch_btn    = add_btn(5, "⬇ Fetch", app.fetch)
    app.settings_btn = add_btn(6, "⚙ Settings", app.open_settings)

    app.pause_btn.state(["disabled"])
    app.stop_btn.state(["disabled"])

    # --------------------------------------------------
    # STATUS BAR
    # --------------------------------------------------
    app.status_var = tk.StringVar(value=C.STATUS_READY)

    status = ttk.Label(
        main,
        textvariable=app.status_var,
        relief="sunken",
        anchor="w"
    )
    status.grid(row=6, column=0, sticky="ew")

    # --------------------------------------------------
    # PROGRESS BAR
    # --------------------------------------------------
    app.progress_var = tk.IntVar(value=0)

    app.progress_bar = ttk.Progressbar(
        main,
        variable=app.progress_var,
        maximum=100,
        mode="determinate"
    )
    app.progress_bar.grid(
        row=7,
        column=0,
        sticky="ew",
        pady=(6, 0)
    )
