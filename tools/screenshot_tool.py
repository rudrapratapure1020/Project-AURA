import pyautogui

def take_screenshot(filename):
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)