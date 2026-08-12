from core.command_normalizer import normalize


def create_plan(command):
    command = command.strip()

    parts = command.split(" and ")

    plan = []

    for part in parts:
        part = part.strip()

        if part:
            normalized = normalize(part)
            plan.append(normalized)

    return plan