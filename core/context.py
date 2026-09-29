from datetime import datetime


class AuraContext:
    def __init__(self):
        self.current_app = None
        self.current_window = None

        # Short-term memory for the current task
        self.history = []
        self.last_command = None
        self.last_result = None

    def set_window(self, app_name, window):
        self.current_app = app_name
        self.current_window = window

        self.history.append({
            "type": "observation",
            "app": app_name,
            "window": window,
            "time": datetime.now().isoformat()
        })

    def clear_window(self):
        self.current_app = None
        self.current_window = None

    def record_command(self, command, result):
        self.last_command = command
        self.last_result = result

        self.history.append({
            "type": "command",
            "command": command,
            "result": result,
            "time": datetime.now().isoformat()
        })

    def get_state(self):
        return {
            "current_app": self.current_app,
            "current_window": self.current_window,
            "last_command": self.last_command,
            "last_result": self.last_result,
            "history": self.history
        }

    def show_state(self):
        print("\n--- AURA CONTEXT ---")
        print(f"Current app: {self.current_app}")
        print(f"Current window: {self.current_window}")
        print(f"Last command: {self.last_command}")
        print(f"Last result: {self.last_result}")
        print(f"History entries: {len(self.history)}")
        print("--------------------\n")