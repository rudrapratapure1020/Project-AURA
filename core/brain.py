def understand(command):
    command = command.strip()
    lower_command = command.lower()

    if lower_command.startswith("open "):
        return {
            "intent": "open",
            "command": command
        }

    if lower_command.startswith("search "):
        return {
            "intent": "search",
            "command": command
        }

    if lower_command.startswith("type "):
        return {
            "intent": "type",
            "command": command
        }

    if lower_command.startswith("copy "):
        return {
            "intent": "copy",
            "command": command
        }

    if lower_command.startswith("move mouse "):
        return {
            "intent": "move_mouse",
            "command": command
        }

    if lower_command == "paste":
        return {
            "intent": "paste",
            "command": command
        }

    if lower_command == "screenshot":
        return {
            "intent": "screenshot",
            "command": command
        }

    if lower_command == "left click":
        return {
            "intent": "left_click",
            "command": command
        }

    if lower_command == "right click":
        return {
            "intent": "right_click",
            "command": command
        }

    if lower_command == "double click":
        return {
            "intent": "double_click",
            "command": command
        }

    if lower_command == "read clipboard":
        return {
            "intent": "read_clipboard",
            "command": command
        }

    if lower_command == "close window":
        return {
            "intent": "close_window",
            "command": command
        }

    if lower_command.startswith("close "):
        return {
            "intent": "close",
            "command": command
        }

    return None