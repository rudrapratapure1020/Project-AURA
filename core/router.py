from tools.browser import search_google
from tools.app_launcher import open_app

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

    else:
        print("Sorry, I don't know that command yet.")