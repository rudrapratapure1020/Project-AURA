import webbrowser
import pyautogui
import time
from urllib.parse import quote


def search_google(query):
    url = f"https://www.google.com/search?q={quote(query)}"

    # Open the URL in the currently active browser
    pyautogui.hotkey("ctrl", "l")
    time.sleep(0.3)

    pyautogui.write(url, interval=0.001)
    pyautogui.press("enter")

    time.sleep(2)

    return True