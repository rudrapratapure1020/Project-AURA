def normalize(command):
    command = command.strip()

    lower_command = command.lower()

    # Remove polite prefixes
    prefixes = [
        "please ",
        "can you ",
        "could you ",
        "would you ",
        "i want you to ",
        "i need you to ",
    ]

    for prefix in prefixes:
        if lower_command.startswith(prefix):
            command = command[len(prefix):].strip()
            break

    # Remove polite suffixes
    suffixes = [
        " please",
        " for me",
    ]

    lower_command = command.lower()

    for suffix in suffixes:
        if lower_command.endswith(suffix):
            command = command[:-len(suffix)].strip()
            break

    lower_command = command.lower()

    # Screenshot variations
    if lower_command in [
        "take a screenshot",
        "take screenshot",
        "capture the screen",
        "capture screen",
    ]:
        return "screenshot"

    # Open variations
    if lower_command.startswith("launch "):
        return "open " + command[7:].strip()

    if lower_command.startswith("start "):
        return "open " + command[6:].strip()

    # Search variations
    if lower_command.startswith("look up "):
        return "search " + command[8:].strip()

    if lower_command.startswith("find "):
        return "search " + command[5:].strip()

    # Type variations
    if lower_command.startswith("write "):
        return "type " + command[6:].strip()

    if lower_command.startswith("enter "):
        return "type " + command[6:].strip()

    return command