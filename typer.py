import time
import pyautogui
import constants as C

pyautogui.PAUSE = 0


def type_text(app, text, delay, char_delay_ms):
    time.sleep(delay)

    app.root.after(0, app.root.lower)
    app.root.after(0, lambda: app.status_var.set(C.STATUS_TYPING))

    open_count = 0

    for ch in text:
        if app.stop_event.is_set():
            app.root.after(0, lambda: app.reset_ui(C.STATUS_STOPPED))
            return

        app.resume_event.wait()

        pyautogui.write(ch)

        if app.coding_mode.get() and ch in C.OPEN_BRACKETS:
            open_count += 1

        if char_delay_ms > 0:
            time.sleep(char_delay_ms / 1000)

    # Coding mode cleanup
    if app.coding_mode.get() and open_count > 0:
        time.sleep(0.2)
        pyautogui.press("del", presses=open_count * 2, interval=0.02)

    app.root.after(0, lambda: app.reset_ui(C.STATUS_FINISHED))
