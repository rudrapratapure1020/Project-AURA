from core.command_registry import COMMANDS
from tools.browser import search_google
from tools.app_launcher import open_app
from tools.keyboard_tool import type_text
from tools.window_tool import close_window, close_app


def handle_command(command):
    command = command.strip()
    lower_command = command.lower()

    print("DEBUG Command:", command)

    if lower_command in COMMANDS:
        COMMANDS[lower_command]()
        return

    if lower_command.startswith("copy "):
        COMMANDS["copy "](command)
        return

    if lower_command.startswith("move mouse "):
        COMMANDS["move mouse"](command)
        return
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
