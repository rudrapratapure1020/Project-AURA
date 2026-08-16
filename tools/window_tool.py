import ctypes
import time

import pyautogui
import pygetwindow as gw

def close_window():
    pyautogui.hotkey("alt", "f4")


def close_app(app_name):
    windows = gw.getWindowsWithTitle(app_name)

    if windows:
        window = windows[0]
        window.activate()
        window.close()
        return True

    return False

def is_app_open(app_name):
    app_name = app_name.lower().strip()

    windows = gw.getAllWindows()

    for window in windows:
        title = window.title.lower().strip()

        if app_name in title:
            return True

    return False

def find_app_window(app_name):
    app_name = app_name.lower().strip()

    windows = gw.getAllWindows()

    for window in windows:
        title = window.title.lower().strip()

        if app_name in title:
            return window

    return None

def activate_window(window):
    try:
        if window is None:
            return False

        if window.isMinimized:
            window.restore()
            time.sleep(0.3)

        hwnd = window._hWnd

        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32

        foreground_hwnd = user32.GetForegroundWindow()

        current_thread = kernel32.GetCurrentThreadId()
        target_thread = user32.GetWindowThreadProcessId(hwnd, None)
        foreground_thread = user32.GetWindowThreadProcessId(
            foreground_hwnd, None
        )

        # Temporarily attach our input thread to the foreground/target
        # window threads so Windows allows the foreground change.
        if foreground_thread != current_thread:
            user32.AttachThreadInput(
                foreground_thread,
                current_thread,
                True
            )

        if target_thread != current_thread:
            user32.AttachThreadInput(
                target_thread,
                current_thread,
                True
            )

        user32.ShowWindow(hwnd, 5)  # SW_SHOW
        user32.SetForegroundWindow(hwnd)
        user32.SetActiveWindow(hwnd)
        user32.SetFocus(hwnd)

        time.sleep(0.5)

        # Detach input threads.
        if target_thread != current_thread:
            user32.AttachThreadInput(
                target_thread,
                current_thread,
                False
            )

        if foreground_thread != current_thread:
            user32.AttachThreadInput(
                foreground_thread,
                current_thread,
                False
            )

        # Verify what Windows actually considers foreground.
        active_hwnd = user32.GetForegroundWindow()

        if active_hwnd == hwnd:
            print(f"DEBUG: {window.title} is foreground.")
            return True

        print(f"DEBUG: Failed to make {window.title} foreground.")
        return False

    except Exception as e:
        print(f"Could not activate window: {e}")
        return False