from core.brain import understand
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

    parts = []

    for part in command.split(" then "):
        part = part.strip()

        if not part:
            continue

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


def rule_based_plan(command):
    """
    Old planner.
    Used as a fallback if the AI brain is unavailable.
    """

    parts = split_command(command)

    plan = []

    for part in parts:
        part = part.strip()

        if part:
            part = part.rstrip(".,!?")
            normalized = normalize(part)
            plan.append(normalized)

    return plan


def create_plan(command, context=None):
    """
    Create an execution plan using the AI brain.

    Falls back to the original rule-based planner
    if the AI brain cannot create a plan.
    """

    print("THINKING...")

    ai_result = understand(command, context)

    if ai_result and "actions" in ai_result:

        plan = []

        for action in ai_result["actions"]:

            action_command = action.get("command", "").strip()

            if not action_command:
                continue

            action_command = action_command.rstrip(".,!?")

            normalized = normalize(action_command)

            plan.append(normalized)

        if plan:
            return plan

    print("AI planning failed. Using fallback planner.")

    return rule_based_plan(command)