
import unittest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from core.planner import split_command
from core.command_registry import find_command
from core.executor import execute
from evaluation.evaluator import AuraEvaluator
from evaluation.task_evaluator import TaskEvaluator


class TestCommandSplitting(unittest.TestCase):

    def test_empty_command(self):
        self.assertEqual(split_command(""), [])

    def test_whitespace_command(self):
        self.assertEqual(split_command("   "), [])

    def test_single_command(self):
        self.assertEqual(split_command("open notepad"), ["open notepad"])

    def test_two_commands(self):
        self.assertEqual(
            split_command("open notepad then type hello"),
            ["open notepad", "type hello"]
        )

    def test_three_commands(self):
        self.assertEqual(
            split_command("open notepad then type hello then close window"),
            ["open notepad", "type hello", "close window"]
        )

    def test_extra_spaces(self):
        self.assertEqual(
            split_command(" open notepad  then  type hello "),
            ["open notepad", "type hello"]
        )

    def test_and_separator(self):
        self.assertEqual(
            split_command("open notepad and type hello"),
            ["open notepad", "type hello"]
        )

    def test_and_inside_search_query(self):
        self.assertEqual(
            split_command("search artificial intelligence and machine learning"),
            ["search artificial intelligence and machine learning"]
        )


class TestCommandRegistry(unittest.TestCase):

    def test_open_command(self):
        handler, needs_command = find_command("open notepad")
        self.assertIsNotNone(handler)
        self.assertTrue(needs_command)

    def test_search_command(self):
        handler, needs_command = find_command("search python")
        self.assertIsNotNone(handler)
        self.assertTrue(needs_command)

    def test_type_command(self):
        handler, needs_command = find_command("type hello")
        self.assertIsNotNone(handler)
        self.assertTrue(needs_command)

    def test_copy_command(self):
        handler, needs_command = find_command("copy hello")
        self.assertIsNotNone(handler)
        self.assertTrue(needs_command)

    def test_close_window_command(self):
        handler, needs_command = find_command("close window")
        self.assertIsNotNone(handler)
        self.assertFalse(needs_command)

    def test_paste_command(self):
        handler, needs_command = find_command("paste")
        self.assertIsNotNone(handler)

    def test_screenshot_command(self):
        handler, needs_command = find_command("screenshot")
        self.assertIsNotNone(handler)

    def test_unsupported_command(self):
        handler, _ = find_command("fly to moon")
        self.assertIsNone(handler)


class TestExecution(unittest.TestCase):

    @patch("core.executor.evaluator.record_result")
    @patch("core.executor.find_command")
    def test_successful_execution(self, mock_find, mock_record):
        mock_find.return_value = (lambda: True, False)
        self.assertTrue(execute("test command"))
        mock_record.assert_called_once()

    @patch("core.executor.evaluator.record_result")
    @patch("core.executor.find_command")
    def test_failed_execution(self, mock_find, mock_record):
        mock_find.return_value = (lambda: False, False)
        self.assertFalse(execute("test command"))

    @patch("core.executor.evaluator.record_result")
    @patch("core.executor.find_command")
    def test_unknown_command(self, mock_find, mock_record):
        mock_find.return_value = (None, False)
        self.assertFalse(execute("unknown command"))

    @patch("core.executor.evaluator.record_result")
    @patch("core.executor.find_command")
    def test_execution_exception(self, mock_find, mock_record):
        def failing_handler():
            raise RuntimeError("Test error")

        mock_find.return_value = (failing_handler, False)
        self.assertFalse(execute("test command"))


class TestCommandMetrics(unittest.TestCase):

    def test_empty_metrics(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "results.json"

            with patch("evaluation.evaluator.RESULTS_FILE", path):
                metrics = AuraEvaluator().get_metrics()

            self.assertEqual(metrics["total_commands"], 0)
            self.assertEqual(metrics["success_rate"], 0)

    def test_record_success(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "results.json"

            with patch("evaluation.evaluator.RESULTS_FILE", path):
                evaluator = AuraEvaluator()
                evaluator.record_result("test", True, evaluator.start_timer())
                metrics = evaluator.get_metrics()

            self.assertEqual(metrics["successful_commands"], 1)

    def test_record_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "results.json"

            with patch("evaluation.evaluator.RESULTS_FILE", path):
                evaluator = AuraEvaluator()
                evaluator.record_result("test", False, evaluator.start_timer())
                metrics = evaluator.get_metrics()

            self.assertEqual(metrics["failed_commands"], 1)


class TestTaskMetrics(unittest.TestCase):

    def test_empty_task_metrics(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tasks.json"

            with patch("evaluation.task_evaluator.RESULTS_FILE", path):
                metrics = TaskEvaluator().get_metrics()

            self.assertEqual(metrics["total_tasks"], 0)

    def test_successful_task(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tasks.json"

            with patch("evaluation.task_evaluator.RESULTS_FILE", path):
                evaluator = TaskEvaluator()
                evaluator.record_task("test task", True, evaluator.start_timer())
                metrics = evaluator.get_metrics()

            self.assertEqual(metrics["completed_tasks"], 1)

    def test_failed_task(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tasks.json"

            with patch("evaluation.task_evaluator.RESULTS_FILE", path):
                evaluator = TaskEvaluator()
                evaluator.record_task("test task", False, evaluator.start_timer())
                metrics = evaluator.get_metrics()

            self.assertEqual(metrics["failed_tasks"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)


class TestRouterIntegration(unittest.TestCase):

    def setUp(self):
        self.patches = [
            patch("core.router.TaskEvaluator"),
        ]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in reversed(self.patches):
            p.stop()

    @patch("core.router.run_agent")
    @patch("core.router.execute")
    @patch("core.router.find_command")
    @patch("core.router.normalize", side_effect=lambda x: x)
    @patch("core.router.split_command", return_value=["open notepad"])
    def test_supported_command_flow(self, *mocks):
        from core.router import handle_command

        split, normalize, find, execute, agent = mocks
        find.return_value = (object(), False)
        execute.return_value = True

        result = handle_command("open notepad")

        self.assertTrue(result)
        execute.assert_called_once_with("open notepad")
        agent.assert_not_called()

    @patch("core.router.run_agent", return_value=True)
    @patch("core.router.execute")
    @patch("core.router.find_command", return_value=(None, False))
    @patch("core.router.normalize", side_effect=lambda x: x)
    @patch("core.router.split_command", return_value=["do something"])
    def test_unsupported_command_uses_agent(self, *mocks):
        from core.router import handle_command

        split, normalize, find, execute, agent = mocks

        result = handle_command("do something")

        self.assertTrue(result)
        agent.assert_called_once_with("do something")
        execute.assert_not_called()

    @patch("core.router.run_agent")
    @patch("core.router.execute", side_effect=[True, True])
    @patch("core.router.find_command", side_effect=[(object(), False), (object(), False)])
    @patch("core.router.normalize", side_effect=lambda x: x)
    @patch(
        "core.router.split_command",
        return_value=["open notepad", "type hello"]
    )
    def test_multi_step_task_flow(self, *mocks):
        from core.router import handle_command

        result = handle_command("open notepad then type hello")

        self.assertTrue(result)
        self.assertEqual(mocks[3].call_count, 2)

    @patch("core.router.run_agent")
    @patch("core.router.execute", side_effect=[True, False])
    @patch("core.router.find_command", return_value=(object(), False))
    @patch("core.router.normalize", side_effect=lambda x: x)
    @patch(
        "core.router.split_command",
        return_value=["open notepad", "type hello", "close window"]
    )
    def test_failed_step_stops_remaining_steps(self, *mocks):
        from core.router import handle_command

        result = handle_command(
            "open notepad then type hello then close window"
        )

        self.assertFalse(result)
        self.assertEqual(mocks[3].call_count, 2)