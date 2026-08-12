from core.command_registry import find_command


def handle_command(command):
    command = command.strip()

    print("DEBUG Command:", command)

    handler, needs_command = find_command(command)

    if handler:
        if needs_command:
            handler(command)
        else:
            handler()

        return

    print("Sorry, I don't know that command yet.")