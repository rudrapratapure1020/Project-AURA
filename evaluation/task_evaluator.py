
import json
import time
from pathlib import Path
from datetime import datetime

RESULTS_FILE = Path(__file__).parent / "task_results.json"


class TaskEvaluator:

    def start_timer(self):
        return time.perf_counter()

    def record_task(self, command, success, start_time):
        duration = round(time.perf_counter() - start_time, 3)

        result = {
            "task": command,
            "success": bool(success),
            "execution_time": duration,
            "timestamp": datetime.now().isoformat()
        }

        if RESULTS_FILE.exists():
            try:
                data = json.loads(RESULTS_FILE.read_text())
            except (json.JSONDecodeError, OSError):
                data = []
        else:
            data = []

        data.append(result)
        RESULTS_FILE.write_text(json.dumps(data, indent=4))

    def get_metrics(self):
        if not RESULTS_FILE.exists():
            data = []
        else:
            try:
                data = json.loads(RESULTS_FILE.read_text())
            except (json.JSONDecodeError, OSError):
                data = []

        total = len(data)
        successful = sum(item["success"] for item in data)

        return {
            "total_tasks": total,
            "completed_tasks": successful,
            "failed_tasks": total - successful,
            "completion_rate": round(
                successful / total * 100, 2
            ) if total else 0,
            "average_task_time": round(
                sum(item["execution_time"] for item in data) / total, 3
            ) if total else 0
        }
