import subprocess
import time
import pygetwindow as gw
from tools.app_discovery import find_app_shortcut


apps = {
    "notepad": "notepad",
    "calculator": "calc",
    "paint": "mspaint"
}


def open_app(app_name):
    print(f"DEBUG: app_name = '{app_name}'")

    app_name = app_name.lower().strip()

    if app_name in apps:
        print(f"DEBUG: Opening {apps[app_name]}")
        subprocess.Popen(apps[app_name])

    else:
        shortcut = find_app_shortcut(app_name)

        if not shortcut:
            print(f"Sorry, I don't know how to open '{app_name}' yet.")
            return False

        print(f"DEBUG: Found application shortcut: {shortcut}")

        import os
        os.startfile(shortcut)

    return True