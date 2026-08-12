from core.planner import create_plan
from core.executor import execute


def run_agent(command, dry_run=False):
    plan = create_plan(command)

    print("PLAN:", plan)

    for step in plan:
        print(f"STEP: {step}")

        if dry_run:
            print("DRY RUN: not executing.")
            continue

        print(f"EXECUTING: {step}")

        success = execute(step)

        if not success:
            print("Agent stopped because a step failed.")
            return False

    if dry_run:
        print("Dry run completed.")
    else:
        print("Agent completed successfully.")

    return True