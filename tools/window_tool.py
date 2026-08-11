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
            