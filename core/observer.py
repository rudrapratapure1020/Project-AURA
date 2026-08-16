import time

from tools.window_tool import find_app_window, activate_window


def observe_app(app_name):
    for attempt in range(5):
        window = find_app_window(app_name)

        if window:
            print(f"OBSERVE: {window.title}")

            if activate_window(window):
                print(f"OBSERVE: {window.title} activated.")
                return window

            print(f"OBSERVE: Could not activate {window.title}.")
            return None

        time.sleep(1)

    print(f"OBSERVE: {app_name} is not open.")
    return None