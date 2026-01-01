import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import threading
import time

pyautogui.PAUSE = 0


class AutoTyperApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Ultra Fast Auto Typer")
        self.root.geometry("520x420")
        self.root.resizable(False, False)

        # control states
        self.pause_event = threading.Event()
        self.stop_event = threading.Event()

        self.typed_count = 0
        self.total_chars = 0
        self.is_running = False

        self.build_ui()
        self.bind_hotkeys()
        self.update_progress()

    # ---------------- UI ----------------
    def build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")

        wrapper = ttk.Frame(self.root, padding=10)
        wrapper.pack(fill="both", expand=True)

        ttk.Label(wrapper, text="Ultra Fast Auto Typer ⚡",
                  font=("Segoe UI", 14, "bold")).pack(pady=5)

        self.text_box = tk.Text(wrapper, height=10, width=55, font=("Consolas", 10))
        self.text_box.pack(pady=8)

        delay_frame = ttk.Frame(wrapper)
        delay_frame.pack()

        ttk.Label(delay_frame, text="Start Delay (seconds): ").pack(side=tk.LEFT)
        self.delay_entry = ttk.Entry(delay_frame, width=6)
        self.delay_entry.insert(0, "2")
        self.delay_entry.pack(side=tk.LEFT)

        self.progress = ttk.Progressbar(wrapper, length=420, mode="determinate")
        self.progress.pack(pady=10)

        btn_frame = ttk.Frame(wrapper)
        btn_frame.pack(pady=10)

        self.start_btn = ttk.Button(btn_frame, text="Start", width=12, command=self.start)
        self.start_btn.grid(row=0, column=0, padx=6)

        self.pause_btn = ttk.Button(btn_frame, text="Pause", width=12, command=self.pause)
        self.pause_btn.grid(row=0, column=1, padx=6)
        self.pause_btn.state(["disabled"])

        self.stop_btn = ttk.Button(btn_frame, text="Stop", width=12, command=self.stop)
        self.stop_btn.grid(row=0, column=2, padx=6)
        self.stop_btn.state(["disabled"])

        self.status_var = tk.StringVar(value="Ready ✨")
        ttk.Label(wrapper, textvariable=self.status_var, anchor="w", relief="groove") \
            .pack(fill="x", pady=5)

    # ---------------- Hotkeys ----------------
    def bind_hotkeys(self):
        self.root.bind("r", lambda e: self.start())
        self.root.bind("p", lambda e: self.pause())
        self.root.bind("s", lambda e: self.stop())

        self.status_var.set("Ready ✨  |  Keys: R=Run, P=Pause/Resume, S=Stop")

    # ------------- Controls -------------
    def start(self):
        if self.is_running:
            return

        text = self.text_box.get("1.0", tk.END).rstrip()
        if not text:
            self.status_var.set("Nothing to type 😅")
            return

        try:
            delay = float(self.delay_entry.get())
            if delay < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Delay", "Delay must be a positive number.")
            return

        self.is_running = True
        self.stop_event.clear()
        self.pause_event.clear()

        self.typed_count = 0
        self.total_chars = len(text)
        self.progress["maximum"] = self.total_chars

        self.status_var.set("Waiting… move your cursor 👆")

        self.start_btn.state(["disabled"])
        self.pause_btn.state(["!disabled"])
        self.stop_btn.state(["!disabled"])

        threading.Thread(
            target=self.type_text,
            args=(text, delay),
            daemon=True
        ).start()

    def pause(self):
        if not self.is_running:
            return

        if self.pause_event.is_set():
            self.pause_event.clear()
            self.pause_btn.config(text="Pause")
        else:
            self.pause_event.set()
            self.pause_btn.config(text="Resume")

    def stop(self):
        self.stop_event.set()
        self.pause_event.clear()
        self.pause_btn.config(text="Pause")

    def reset_ui(self, msg):
        self.is_running = False
        self.start_btn.state(["!disabled"])
        self.pause_btn.state(["disabled"])
        self.stop_btn.state(["disabled"])
        self.status_var.set(msg)

    # ------------- Typing Engine -------------
    def type_text(self, text, delay):
        time.sleep(delay)

        self.root.after(0, self.root.lower)
        self.root.after(0, lambda: self.status_var.set("Typing… 🔥"))

        for ch in text:
            if self.stop_event.is_set():
                self.root.after(0, lambda: self.reset_ui("Stopped ❌"))
                return

            while self.pause_event.is_set() and not self.stop_event.is_set():
                time.sleep(0.03)

            pyautogui.write(ch)
            self.typed_count += 1

        self.root.after(0, lambda: self.reset_ui("Finished ✅"))

    # -------- Progress updater --------
    def update_progress(self):
        self.progress["value"] = self.typed_count
        self.root.after(40, self.update_progress)


root = tk.Tk()
app = AutoTyperApp(root)
root.mainloop()
