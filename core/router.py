from tools.browser import search_google
from tools.app_launcher import open_app
from tools.keyboard_tool import type_text
from tools.mouse_tool import move_mouse, left_click, right_click, double_click

def handle_command(command):
    print("DEBUG Command:", command)

    if command.lower().startswith("search "):
        print("Detected SEARCH command")
        query = command[7:]
        search_google(query)

    elif command.lower().startswith("open "):
        print("Detected OPEN command")
        app_name = command[5:]
        open_app(app_name)

    elif command.lower().startswith("type "):
        text = command[5:].strip()
        type_text(text)

    elif command.lower() == "left click":
        left_click()

    elif command.lower() == "right click":
        right_click()

    elif command.lower() == "double click":
        double_click()

    elif command.lower().startswith("move mouse "):
        parts = command.split()

        try:
            x = int(parts[2])
            y = int(parts[3])

            move_mouse(x, y)

        except (ValueError, IndexError):
            print("Sorry, please provide valid mouse coordinates.")

    else:
        print("Sorry, I don't know that command yet.")