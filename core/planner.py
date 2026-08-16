from core.command_normalizer import normalize


COMMAND_STARTS = (
    "open ",
    "launch ",
    "start ",
    "type ",
    "write ",
    "enter ",
    "search ",
    "look up ",
    "find ",
    "copy ",
    "paste",
    "screenshot",
    "take a screenshot",
    "capture screen",
    "left click",
    "right click",
    "double click",
    "move mouse ",
    "close ",
    "close window",
    "read clipboard",
)


def is_command_start(text):
    text = text.strip().lower()

    return text.startswith(COMMAND_STARTS)


def split_command(command):
    command = command.strip()

    # First split on "then" because it clearly indicates
    # that another action follows.
    parts = []

    for part in command.split(" then "):
        part = part.strip()

        if not part:
            continue

        # Only split "and" when the following text looks
        # like another AURA command.
        current = part

        while " and " in current.lower():
            lower_current = current.lower()
            index = lower_current.find(" and ")

            before = current[:index].strip()
            after = current[index + 5:].strip()

            if is_command_start(after):
                parts.append(before)
                current = after
            else:
                break

        if current:
            parts.append(current)

    return parts


def create_plan(command):
    parts = split_command(command)

    plan = []

    for part in parts:
        part = part.strip()

        if part:
            part = part.rstrip(".,!?")

            normalized = normalize(part)
            plan.append(normalized)

    return plan