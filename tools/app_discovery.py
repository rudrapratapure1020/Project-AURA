from pathlib import Path


START_MENU_LOCATIONS = [
    Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs",
    Path("C:/ProgramData/Microsoft/Windows/Start Menu/Programs"),
]


def find_app_shortcut(app_name):
    app_name = app_name.lower().strip()

    for location in START_MENU_LOCATIONS:
        if not location.exists():
            continue

        for shortcut in location.rglob("*.lnk"):
            if app_name in shortcut.stem.lower():
                return shortcut

    return None

def launch_discovered_app(app_name):
    shortcut = find_app_shortcut(app_name)

    if not shortcut:
        print(f"DISCOVERY: Could not find '{app_name}'.")
        return False

    print(f"DISCOVERY: Found {shortcut}")

    import os
    os.startfile(shortcut)

    return True