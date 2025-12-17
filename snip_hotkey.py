import os
import datetime
import time
from pathlib import Path
from PIL import ImageGrab
import keyboard

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SAVE_DIR = SCRIPT_DIR.parent.parent / "snips"
DEFAULT_LOG_PATH = SCRIPT_DIR / "snip_hotkey.log"

SAVE_DIR = Path(os.getenv("SNIP_HOTKEY_SAVE_DIR", str(DEFAULT_SAVE_DIR)))
LOG_PATH = Path(os.getenv("SNIP_HOTKEY_LOG_PATH", str(DEFAULT_LOG_PATH)))
SAVE_DIR.mkdir(parents=True, exist_ok=True)


def log(message: str) -> None:
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {message}\n")
    except Exception:
        pass


def save_clipboard_image():
    log("F8 pressed")
    img = None
    for attempt in range(5):
        try:
            img = ImageGrab.grabclipboard()
        except Exception as e:
            log(f"grabclipboard failed: {e}")
            return
        if img is not None:
            break
        time.sleep(0.1)
    if img is None:
        log("no image in clipboard after retries")
        return

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(SAVE_DIR, f"snip_{ts}.png")
    try:
        img.save(path, "PNG")
        log(f"saved image -> {path}")
    except Exception as e:
        log(f"save failed: {e}")
        return

    try:
        keyboard.write(f'"{path}"')
        log("typed path into active window")
    except Exception as e:
        log(f"keyboard.write failed: {e}")


def main():
    log("snip_hotkey started (F8)")
    try:
        keyboard.add_hotkey("f8", save_clipboard_image)
        log("hotkey registered")
        keyboard.wait()
    except KeyboardInterrupt:
        log("snip_hotkey stopped by KeyboardInterrupt")
    except Exception as e:
        log(f"add_hotkey failed or runtime error: {e}")


if __name__ == "__main__":
    main()
