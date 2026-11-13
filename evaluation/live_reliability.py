
import json
import time
from pathlib import Path
from datetime import datetime

from core.router import handle_command

RESULTS_FILE = Path(__file__).parent / "live_reliability_results.json"

TEST_COMMANDS = [
    "open notepad",
    "open calculator",
    "open paint",
]

ROUNDS = 3


def run_benchmark():
    results = []

    print("\n===== AURA LIVE RELIABILITY TEST =====")

    for round_no in range(1, ROUNDS + 1):
        print(f"\n--- Round {round_no}/{ROUNDS} ---")

        for command in TEST_COMMANDS:
            start = time.perf_counter()

            try:
                success = handle_command(command)
                success = success is True
                error = None
            except Exception as e:
                success = False
                error = str(e)

            duration = round(time.perf_counter() - start, 3)

            result = {
                "round": round_no,
                "command": command,
                "success": success,
                "execution_time": duration,
                "error": error,
                "timestamp": datetime.now().isoformat()
            }

            results.append(result)

            status = "PASS" if success else "FAIL"
            print(f"{status}: {command} ({duration}s)")

    total = len(results)
    passed = sum(r["success"] for r in results)

    report = {
        "date": datetime.now().isoformat(),
        "total_tests": total,
        "passed": passed,
        "failed": total - passed,
        "success_rate": round(passed / total * 100, 2),
        "results": results
    }

    RESULTS_FILE.write_text(json.dumps(report, indent=4))

    print("\n===== FINAL REPORT =====")
    print(f"Total tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success rate: {report['success_rate']}%")
    print(f"Average time: {round(sum(r['execution_time'] for r in results) / total, 3)}s")
    print(f"Saved to: {RESULTS_FILE}")


if __name__ == "__main__":
    run_benchmark()
