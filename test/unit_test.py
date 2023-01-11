"""
Runs the unit tests of every file used for the CPU
"""

from pathlib import Path
import itertools
from digital import run_digital_tests


FORMAT_BOLD_RED = "\x1B[1;91m"
FORMAT_BOLD_GREEN = "\x1B[1;92m"
FORMAT_BOLD_YELLOW = "\x1B[1;93m"
FORMAT_END = "\x1B[0m"


SRC_DIR = Path(__file__).parent.parent / "src"
LIB_DIR = Path(__file__).parent.parent / "lib"
EXCLUDED = {SRC_DIR / "main.dig"}


def main() -> None:
    """Runs the unit tests of all of the Digital files"""

    num_failed = 0
    num_run = 0
    for dig_file in itertools.chain(SRC_DIR.glob("**/*.dig"), LIB_DIR.glob("**/*.dig")):
        if dig_file in EXCLUDED:
            continue
        print(f"{FORMAT_BOLD_YELLOW}Running unit tests in '{dig_file}'{FORMAT_END}")

        result = run_digital_tests(dig_file)
        num_run += 1
        if not result:
            print(f"{FORMAT_BOLD_RED}Unit tests in '{dig_file}' failed.{FORMAT_END}")
            num_failed += 1

    if num_failed == 0:
        print(
            f"{FORMAT_BOLD_GREEN}All unit tests passed ({num_run}/{num_run}){FORMAT_END}"
        )
    else:
        num_success = num_run - num_failed
        print(
            f"{FORMAT_BOLD_RED}Some unit tests failed ({num_success}/{num_run}){FORMAT_END}"
        )


if __name__ == "__main__":
    main()
