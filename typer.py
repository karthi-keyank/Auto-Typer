import time
import pyautogui
import constants as C

pyautogui.PAUSE = 0


def type_text(app, text, start_delay, char_delay_ms):
    """
    Background typing worker.
    """

    # Lazy import to avoid circular dependency
    from controllers.typing_controller import reset_ui

    time.sleep(start_delay)

    # setup progress
    app.progress_max = max(len(text), 1)
    app.typed_count = 0

    app.root.after(0, app.root.lower)
    app.root.after(0, lambda: app.status_var.set(C.STATUS_TYPING))

    open_count = 0

    for ch in text:
        if app.stop_event.is_set():
            app.root.after(
                0,
                lambda: reset_ui(app, C.STATUS_STOPPED)
            )
            return

        app.resume_event.wait()

        pyautogui.write(ch)
        app.typed_count += 1

        if app.coding_mode.get() and ch in C.OPEN_BRACKETS:
            open_count += 1

        if char_delay_ms > 0:
            time.sleep(char_delay_ms / 1000)

    # Coding mode cleanup
    if app.coding_mode.get() and open_count > 0:
        time.sleep(0.2)
        pyautogui.press(
            "del",
            presses=open_count * 2,
            interval=0.02
        )

    app.root.after(
        0,
        lambda: reset_ui(app, C.STATUS_FINISHED)
    )
