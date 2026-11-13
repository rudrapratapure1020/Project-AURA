
import json
import time
from pathlib import Path
from datetime import datetime

import pyautogui

from core.router import handle_command
from tools.clipboard_tool import get_clipboard

RESULTS_FILE = Path(__file__).parent / "workflow_results.json"

def run_test():
    steps = []

    def test_step(name, action):
        try:
            result = action()
            passed = result is True
        except Exception as e:
            passed = False
            print(f"{name}: ERROR - {e}")

        steps.append({"step": name, "passed": passed})
        print(f"{'PASS' if passed else 'FAIL'}: {name}")
        return passed

    print("\n===== AURA WORKFLOW BENCHMARK =====")

    test_step(
        "Open Notepad",
        lambda: handle_command("open notepad")
    )

    time.sleep(1)

    test_step(
        "Type text",
        lambda: handle_command("type AURA workflow benchmark test")
    )

    test_step(
        "Copy text",
        lambda: handle_command("copy AURA clipboard verification")
    )

    clipboard_ok = test_step(
        "Verify clipboard",
        lambda: get_clipboard() == "AURA clipboard verification"
    )

    test_step(
        "Paste text",
        lambda: handle_command("paste")
    )

    # Clear test text to avoid a save prompt.
    try:
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("backspace")
        time.sleep(0.3)
    except Exception as e:
        print("Cleanup warning:", e)

    test_step(
        "Close Notepad",
        lambda: handle_command("close window")
    )

    total = len(steps)
    passed = sum(s["passed"] for s in steps)

    report = {
        "date": datetime.now().isoformat(),
        "total_steps": total,
        "passed": passed,
        "failed": total - passed,
        "success_rate": round(passed / total * 100, 2),
        "clipboard_verified": clipboard_ok,
        "steps": steps
    }

    RESULTS_FILE.write_text(json.dumps(report, indent=4))

    print("\n===== FINAL RESULTS =====")
    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success rate: {report['success_rate']}%")
    print(f"Report: {RESULTS_FILE}")


if __name__ == "__main__":
    run_test()

