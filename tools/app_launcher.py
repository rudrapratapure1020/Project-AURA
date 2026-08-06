import subprocess

def open_app(app_name):
    if app_name.lower() == "notepad":
        subprocess.Popen("notepad")

    else:
        print(f"Sorry, I don't know how to open '{app_name}' yet.")