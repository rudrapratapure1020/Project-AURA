
from core.command_normalizer import normalize
from core.command_registry import find_command
from core.agent import run_agent
from core.executor import execute
from core.planner import split_command
from evaluation.task_evaluator import TaskEvaluator


def handle_command(command):
    command = command.strip()

    if not command:
        return

    evaluator = TaskEvaluator()
    start_time = evaluator.start_timer()
    task_success = False

    try:
        print("DEBUG Command:", command)

        commands = split_command(command)

        if len(commands) > 1:
            task_success = True

            for item in commands:
                normalized = normalize(item)
                print("DEBUG Step:", normalized)

                handler, needs_command = find_command(normalized)

                if handler:
                    result = execute(normalized)
                else:
                    result = run_agent(normalized)

                if result is False:
                    task_success = False
                    break

            return task_success

        normalized_command = normalize(command)

        print("DEBUG Normalized:", normalized_command)

        handler, needs_command = find_command(normalized_command)

        if handler:
            result = execute(normalized_command)
        else:
            result = run_agent(normalized_command)

        task_success = result is not False
        return task_success

    finally:
        evaluator.record_task(
            command,
            task_success,
            start_time
        )
