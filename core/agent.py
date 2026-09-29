from core.planner import create_plan
from core.executor import execute
from core.context import AuraContext


def run_agent(command, dry_run=False):
    context = AuraContext()

    print("\nAURA STARTED")
    print(f"REQUEST: {command}\n")

    plan = create_plan(command, context)

    if not plan:
        print("AURA could not create a plan.")
        return False

    print("PLAN:", plan)

    for step in plan:
        print(f"\nSTEP: {step}")

        if dry_run:
            print("DRY RUN: not executing.")
            continue

        print(f"EXECUTING: {step}")

        success = execute(step, context)

        if not success:
            print("Agent stopped because a step failed.")
            context.show_state()
            return False

    print("\nTASK COMPLETED")
    context.show_state()

    return True