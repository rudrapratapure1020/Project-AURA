from core.brain import understand
from core.executor import execute_tool
from core.context import AuraContext


def run_agent(command, dry_run=False):

    context = AuraContext()

    print("\n==============================")
    print("        AURA STARTED")
    print("==============================")

    print(f"\nREQUEST: {command}")

    print("\nTHINKING...")

    plan = understand(command, context)

    if not plan or "actions" not in plan:
        print("AURA could not create a plan.")
        return False

    print("\nAI PLAN:")

    for action in plan["actions"]:
        print(
            f"  → {action['tool']} "
            f"{action.get('arguments', {})}"
        )

    for action in plan["actions"]:

        tool_name = action.get("tool")
        arguments = action.get("arguments", {})

        print("\n--------------------------------")
        print(f"TOOL: {tool_name}")
        print(f"ARGUMENTS: {arguments}")
        print("--------------------------------")

        if dry_run:
            print("DRY RUN: tool not executed.")
            continue

        result = execute_tool(
            tool_name,
            arguments,
            context
        )

        print(f"RESULT: {result}")

        if not result.get("success", False):
            print("\nAURA stopped because the tool failed.")
            context.show_state()
            return False

    print("\n==============================")
    print("       TASK COMPLETED")
    print("==============================")

    context.show_state()

    return True