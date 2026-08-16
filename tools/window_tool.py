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
        window.activate()
        return True
    except Exception as e:
        print(f"Could not activate window: {e}")
        return False