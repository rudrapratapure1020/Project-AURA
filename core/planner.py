from core.command_normalizer import normalize


def create_plan(command):
    command = command.strip()

    separators = [
        " and ",
        " then ",
    ]

    parts = [command]

    for separator in separators:
        new_parts = []

        for part in parts:
            new_parts.extend(part.split(separator))

        parts = new_parts

    plan = []

    for part in parts:
        part = part.strip()

        if part:
            normalized = normalize(part)
            plan.append(normalized)

    return plan