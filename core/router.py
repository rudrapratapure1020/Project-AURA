from tools.browser import search_google
from tools.app_launcher import open_app
from tools.keyboard_tool import type_text
from tools.mouse_tool import (
    move_mouse,
    left_click,
    right_click,
    double_click
)
from tools.clipboard_tool import (
    copy_text,
    get_clipboard,
    paste_text
)
from tools.screenshot_tool import take_screenshot
from tools.window_tool import close_window, close_app


def handle_command(command):
    command = command.strip()
    lower_command = command.lower()

    print("DEBUG Command:", command)

    if lower_command.startswith("search "):
        print("Detected SEARCH command")
        query = command[7:].strip()
        search_google(query)

    elif lower_command.startswith("open "):
        print("Detected OPEN command")
        app_name = command[5:].strip()
        open_app(app_name)

    elif lower_command.startswith("type "):
        text = command[5:].strip()
        type_text(text)

    elif lower_command == "left click":
        left_click()

    elif lower_command == "right click":
        right_click()

    elif lower_command == "double click":
        double_click()

    elif lower_command.startswith("move mouse "):
        parts = command.split()

        try:
            x = int(parts[2])
            y = int(parts[3])
            move_mouse(x, y)

        except (ValueError, IndexError):
            print("Sorry, please provide valid mouse coordinates.")

    elif lower_command.startswith("copy "):
        text = command[5:].strip()
        copy_text(text)
        print("Text copied to clipboard.")

    elif lower_command == "paste":
        paste_text()

    elif lower_command == "read clipboard":
        text = get_clipboard()
        print(f"Clipboard: {text}")

    elif lower_command == "screenshot":
        take_screenshot("screenshot.png")
        print("Screenshot saved as screenshot.png")

    elif lower_command == "close window":
        close_window()

    elif lower_command.startswith("close "):
        app_name = command[6:].strip()

        if close_app(app_name):
            print(f"{app_name} closed successfully.")
        else:
            print(f"I couldn't find '{app_name}'.")

    else:
        print("Sorry, I don't know that command yet.")
