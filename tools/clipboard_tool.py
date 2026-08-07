import pyperclip
import pyautogui


def copy_text(text):
    pyperclip.copy(text)


def get_clipboard():
    return pyperclip.paste()

def paste_text():
    pyautogui.hotkey("ctrl", "v")