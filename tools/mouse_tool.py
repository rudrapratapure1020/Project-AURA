import pyautogui


def move_mouse(x, y):
    pyautogui.moveTo(x, y)


def left_click():
    pyautogui.click()


def right_click():
    pyautogui.rightClick()


def double_click():
    pyautogui.doubleClick()