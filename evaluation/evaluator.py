
import json
import time
from pathlib import Path
from datetime import datetime

RESULTS_FILE = Path(__file__).parent / "results.json"


class AuraEvaluator:

    def __init__(self):
        self.results = []

    def start_timer(self):
        return time.perf_counter()

    def record_result(self, command, success, start_time):
        execution_time = round(time.perf_counter() - start_time, 3)

        result = {
            "command": command,
            "success": bool(success),
            "execution_time": execution_time,
            "timestamp": datetime.now().isoformat()
        }

        self.results.append(result)
        self._save_results()

        return result

    def _save_results(self):
        if RESULTS_FILE.exists():
            try:
                existing = json.loads(RESULTS_FILE.read_text())
            except (json.JSONDecodeError, OSError):
                existing = []
        else:
            existing = []

        existing.extend(self.results)
        RESULTS_FILE.write_text(json.dumps(existing, indent=4))
        self.results.clear()

    
    def get_metrics(self):
        if RESULTS_FILE.exists():
            try:
                data = json.loads(RESULTS_FILE.read_text())
            except (json.JSONDecodeError, OSError):
                data = []
        else:
            data = []

        total = len(data)
        successful = sum(item["success"] for item in data)

        return {
            "total_commands": total,
            "successful_commands": successful,
            "failed_commands": total - successful,
            "success_rate": round(successful / total * 100, 2) if total else 0,
            "average_execution_time": round(
                sum(item["execution_time"] for item in data) / total, 3
            ) if total else 0
        }
