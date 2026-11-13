
from core.command_registry import find_command
from evaluation.evaluator import AuraEvaluator

evaluator = AuraEvaluator()


def execute(command, context=None):
    start_time = evaluator.start_timer()

    def finish(success):
        evaluator.record_result(command, success, start_time)

        if context:
            context.record_command(command, success)

        return success

    handler, needs_command = find_command(command)

    if not handler:
        print(f"I don't know how to execute: {command}")
        return finish(False)

    try:
        if needs_command:
            try:
                result = handler(command, context)
            except TypeError:
                result = handler(command)
        else:
            result = handler()

    except Exception as e:
        print(f"EXECUTION ERROR: {e}")
        return finish(False)

    if result is False:
        return finish(False)

    return finish(True)
