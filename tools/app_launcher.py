import subprocess

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
        print(f"Sorry, I don't know how to open '{app_name}' yet.")