from core.command_registry import find_command


def execute(command, context=None):
    handler, needs_command = find_command(command)

    if not handler:
        print(f"I don't know how to execute: {command}")

        if context:
            context.record_command(command, False)

        return False

    try:
        if needs_command:
            try:
                result = handler(command, context)
            except TypeError:
                result = handler(command)
        else:
            result = handler()

    except Exception as e:
        print(f"EXECUTION ERROR: {e}")

        if context:
            context.record_command(command, False)

        return False

    if result is False:
        if context:
            context.record_command(command, False)
        return False

    if context:
        context.record_command(command, True)

    return True