import os
import datetime
import time
import ctypes
from ctypes import wintypes
from pathlib import Path
from PIL import ImageGrab
import keyboard

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SAVE_DIR = Path(os.path.expanduser("~")) / "Documents" / "snips"
DEFAULT_LOG_PATH = SCRIPT_DIR / "snip_hotkey.log"

SAVE_DIR = Path(os.getenv("SNIP_HOTKEY_SAVE_DIR", str(DEFAULT_SAVE_DIR)))
LOG_PATH = Path(os.getenv("SNIP_HOTKEY_LOG_PATH", str(DEFAULT_LOG_PATH)))
SAVE_DIR.mkdir(parents=True, exist_ok=True)

# Win32 hotkey constants
MOD_NONE = 0x0000
WM_HOTKEY = 0x0312
VK_F8 = 0x77
HOTKEY_ID = 1


class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", wintypes.HWND),
        ("message", wintypes.UINT),
        ("wParam", wintypes.WPARAM),
        ("lParam", wintypes.LPARAM),
        ("time", wintypes.DWORD),
        ("pt", wintypes.POINT),
    ]


# Win32 bindings
user32 = ctypes.windll.user32
GetMessageW = user32.GetMessageW
GetMessageW.restype = wintypes.BOOL
GetMessageW.argtypes = [ctypes.POINTER(MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT]
RegisterHotKey = user32.RegisterHotKey
RegisterHotKey.restype = wintypes.BOOL
RegisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int, wintypes.UINT, wintypes.UINT]
UnregisterHotKey = user32.UnregisterHotKey
UnregisterHotKey.restype = wintypes.BOOL
UnregisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int]


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

    if not RegisterHotKey(None, HOTKEY_ID, MOD_NONE, VK_F8):
        log("RegisterHotKey failed (F8)")
        return

    log("hotkey registered (Win32)")
    msg = MSG()
    try:
        while True:
            result = GetMessageW(ctypes.byref(msg), None, 0, 0)
            if result == 0:
                break  # WM_QUIT
            if result == -1:
                log("GetMessage failed")
                break
            if msg.message == WM_HOTKEY and msg.wParam == HOTKEY_ID:
                save_clipboard_image()
    except KeyboardInterrupt:
        log("snip_hotkey stopped by KeyboardInterrupt")
    except Exception as e:
        log(f"runtime error: {e}")
    finally:
        UnregisterHotKey(None, HOTKEY_ID)
        log("hotkey unregistered")


if __name__ == "__main__":
    main()
