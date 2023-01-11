"""
Tests the Digital simulator implementation of the CPU
"""

from pathlib import Path
import time
import sys
from simulatortester import SimulatorTester
from digital import run_digital
from tests.runtests import run_tests

MAIN_FILE = Path(__file__).parent.parent / "src" / "main.dig"


def main() -> None:
    """Run the tests on the simulator"""

    print("Starting Digital...")
    with run_digital(MAIN_FILE) as digital_proc:
        time.sleep(2)
        tester = SimulatorTester()

        success = run_tests(tester)

        print("Stopping Digital")
        digital_proc.kill()

        if not success:
            sys.exit(1)


if __name__ == "__main__":
    main()
