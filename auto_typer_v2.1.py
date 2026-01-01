import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import threading
import time

pyautogui.PAUSE = 0


class AutoTyperApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Auto Typer")

        self.root.geometry("700x550")
        self.root.minsize(650, 520)
        self.root.resizable(True, True)

        self.stop_event = threading.Event()
        self.resume_event = threading.Event()
        self.resume_event.set()

        self.typed_count = 0
        self.total_chars = 0
        self.is_running = False
        self.bracket_count = 0

        self.build_ui()
        self.bind_hotkeys()
        self.update_progress()

    def build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")

        wrapper = ttk.Frame(self.root, padding=12)
        wrapper.grid(row=0, column=0, sticky="nsew")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        wrapper.grid_rowconfigure(2, weight=1)

        ttk.Label(wrapper, text="Auto Typer",
                  font=("Segoe UI", 16, "bold")).grid(row=0, column=0, pady=6, sticky="w")

        text_frame = ttk.Frame(wrapper)
        text_frame.grid(row=2, column=0, sticky="nsew", pady=6)

        text_scroll = ttk.Scrollbar(text_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_box = tk.Text(
            text_frame,
            height=12,
            font=("Consolas", 11),
            wrap="word",
            yscrollcommand=text_scroll.set
        )
        self.text_box.pack(fill="both", expand=True)
        text_scroll.config(command=self.text_box.yview)

        controls = ttk.Frame(wrapper)
        controls.grid(row=3, column=0, pady=6, sticky="w")

        ttk.Label(controls, text="Start Delay (sec): ").grid(row=0, column=0, padx=4)
        self.delay_entry = ttk.Entry(controls, width=7)
        self.delay_entry.insert(0, "2")
        self.delay_entry.grid(row=0, column=1, padx=4)

        ttk.Label(controls, text="Character Delay (ms): ").grid(row=0, column=2, padx=6)
        self.char_delay_entry = ttk.Entry(controls, width=7)
        self.char_delay_entry.insert(0, "0")
        self.char_delay_entry.grid(row=0, column=3, padx=4)

        self.coding_mode = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            wrapper,
            text="Coding mode (auto delete paired brackets)",
            variable=self.coding_mode
        ).grid(row=4, column=0, pady=4, sticky="w")

        self.progress = ttk.Progressbar(wrapper, mode="determinate")
        self.progress.grid(row=5, column=0, pady=10, sticky="ew")

        btns = ttk.Frame(wrapper)
        btns.grid(row=6, column=0, pady=8)

        self.start_btn = ttk.Button(btns, text="Start", width=14, command=self.start)
        self.start_btn.grid(row=0, column=0, padx=8)

        self.pause_btn = ttk.Button(btns, text="Pause", width=14, command=self.pause)
        self.pause_btn.grid(row=0, column=1, padx=8)
        self.pause_btn.state(["disabled"])

        self.stop_btn = ttk.Button(btns, text="Stop", width=14, command=self.stop)
        self.stop_btn.grid(row=0, column=2, padx=8)
        self.stop_btn.state(["disabled"])
        self.restart_btn = ttk.Button(btns, text="Restart", width=14, command=self.restart)
        self.restart_btn.grid(row=0, column=3, padx=8)
        self.status_var = tk.StringVar(value="Ready ✨")
        ttk.Label(wrapper, textvariable=self.status_var,
                  anchor="w", relief="groove").grid(row=7, column=0, sticky="ew", pady=6)

    def bind_hotkeys(self):
        self.root.bind("r", lambda e: self.restart()) 
        self.root.bind("p", lambda e: self.pause())
        self.root.bind("s", lambda e: self.stop())
        self.status_var.set("Ready   |  Keys: R=Restart, P=Pause/Resume, S=Stop")

    def start(self):
        if self.is_running:
            return

        text = self.text_box.get("1.0", tk.END).rstrip()
        if not text:
            self.status_var.set("Nothing to type")
            return

        try:
            delay = float(self.delay_entry.get())
            if delay < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Delay", "Delay must be positive.")
            return

        try:
            char_delay_ms = float(self.char_delay_entry.get())
            if char_delay_ms < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Delay", "Character delay must be zero or positive.")
            return

        self.is_running = True
        self.stop_event.clear()
        self.resume_event.set()

        self.typed_count = 0
        self.total_chars = len(text)
        self.progress["maximum"] = self.total_chars
        self.bracket_count = 0

        self.status_var.set("Waiting… move your cursor")

        self.start_btn.state(["disabled"])
        self.pause_btn.state(["!disabled"])
        self.stop_btn.state(["!disabled"])

        threading.Thread(
            target=self.type_text,
            args=(text, delay, char_delay_ms),
            daemon=True
        ).start()

    def pause(self):
        if not self.is_running:
            return
        if self.resume_event.is_set():
            self.resume_event.clear()
            self.pause_btn.config(text="Resume")
        else:
            self.resume_event.set()
            self.pause_btn.config(text="Pause")

    def stop(self):
        self.stop_event.set()
        self.resume_event.set()
        self.pause_btn.config(text="Pause")

    def restart(self):
        self.stop_event.set()
        self.resume_event.set()
        self.pause_btn.config(text="Pause")

        time.sleep(0.05)

        self.is_running = False
        self.start()

    def reset_ui(self, msg):
        self.is_running = False
        self.start_btn.state(["!disabled"])
        self.pause_btn.state(["disabled"])
        self.stop_btn.state(["disabled"])
        self.status_var.set(msg)

    def type_text(self, text, delay, char_delay_ms):
        time.sleep(delay)

        self.root.after(0, self.root.lower)
        self.root.after(0, lambda: self.status_var.set("Typing… "))

        for ch in text:
            if self.stop_event.is_set():
                self.root.after(0, lambda: self.reset_ui("Stopped "))
                return

            self.resume_event.wait()

            if self.coding_mode.get() and ch in "([{":
                self.bracket_count += 1

            pyautogui.write(ch)
            self.typed_count += 1

            if char_delay_ms > 0:
                time.sleep(char_delay_ms / 1000.0)

        if self.coding_mode.get() and self.bracket_count > 0:
            deletes = self.bracket_count * 2
            pyautogui.press("delete", presses=deletes, interval=0)

        self.root.after(0, lambda: self.reset_ui("Finished"))

    def update_progress(self):
        self.progress["value"] = self.typed_count
        self.root.after(40, self.update_progress)


root = tk.Tk()
app = AutoTyperApp(root)
root.mainloop()
