import pyautogui
import time


def type_text(text):
    time.sleep(3)
    pyautogui.write(text, interval=0.05)
    return True