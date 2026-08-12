from tools.clipboard_tool import copy_text, get_clipboard, paste_text
from tools.mouse_tool import left_click, right_click, double_click
from tools.mouse_tool import move_mouse
from tools.screenshot_tool import take_screenshot
from tools.keyboard_tool import type_text
from tools.browser import search_google

def handle_search(command):
    query = command[7:].strip()
    search_google(query)

def handle_type(command):
    text = command[5:].strip()
    type_text(text)

def handle_copy(command):
    text = command[5:].strip()
    copy_text(text)
    print("Text copied to clipboard.")

def handle_move_mouse(command):
    parts = command.split()

    try:
        x = int(parts[2])
        y = int(parts[3])

        move_mouse(x, y)

    except (ValueError, IndexError):
        print("Sorry, please provide valid mouse coordinates.")

COMMANDS = {
    "copy ": handle_copy,
    "paste": paste_text,
    "search ": handle_search,
    "type ": handle_type,
    "screenshot": lambda: take_screenshot("screenshot.png"),
    "left click": left_click,
    "right click": right_click,
    "double click": double_click,
    "move mouse ": handle_move_mouse,
    "read clipboard": lambda: print(
        f"Clipboard: {get_clipboard()}"
    ),
}

def find_command(command):
    lower_command = command.lower().strip()

    # Exact commands
    for pattern, handler in COMMANDS.items():

        if not pattern.endswith(" "):
            if lower_command == pattern:
                return handler, False

    # Commands that accept arguments
    for pattern, handler in COMMANDS.items():

        if pattern.endswith(" "):
            prefix = pattern.rstrip()

            if lower_command.startswith(prefix + " "):
                return handler, True

    return None, False