from core.command_normalizer import normalize
from core.brain import understand
from core.command_registry import find_command
from core.agent import run_agent

def handle_command(command):
    command = command.strip()

    print("DEBUG Command:", command)

    if " and " in command.lower():
        run_agent(command)
        return

    normalized_command = normalize(command)

    print("DEBUG Normalized:", normalized_command)

    understanding = understand(normalized_command)

    if understanding is None:
        print("Sorry, I don't know that command yet.")
        return

    handler, needs_command = find_command(normalized_command)

    if handler:
        if needs_command:
            handler(normalized_command)
        else:
            handler()

        return

    print("I understood the command, but I don't know how to execute it yet.")