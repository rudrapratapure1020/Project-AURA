import time

from tools.window_tool import is_app_open


def observe_app(app_name):
    for attempt in range(5):
        if is_app_open(app_name):
            print(f"OBSERVE: {app_name} is open.")
            return True

        time.sleep(1)

    print(f"OBSERVE: {app_name} is not open.")
    return False