from core.command_registry import find_command


def execute(command):
    handler, needs_command = find_command(command)

    if not handler:
        print(f"I don't know how to execute: {command}")
        return False

    if needs_command:
        result = handler(command)
    else:
        result = handler()

    if result is False:
        return False

    return True