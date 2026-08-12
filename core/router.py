from core.command_registry import find_command
from tools.app_launcher import open_app
from tools.window_tool import close_window, close_app


def handle_command(command):
    command = command.strip()
    lower_command = command.lower()

    print("DEBUG Command:", command)

    handler, needs_command = find_command(command)

    if handler: 
        if needs_command:
            handler(command)
        else:
            handler()

        return

    elif lower_command.startswith("open "):
        print("Detected OPEN command")
        app_name = command[5:].strip()
        open_app(app_name)

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
