from tools.browser import search_google
from tools.app_launcher import open_app
from tools.keyboard_tool import type_text

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

    else:
        print("Sorry, I don't know that command yet.")