"""
Tests the Digital simulator implementation of the CPU
"""

import subprocess
import urllib.request as urllib
from zipfile import ZipFile
from pathlib import Path
import time
import sys
from simulatortester import SimulatorTester
from tests.runtests import run_tests

DIGITAL_URL = "https://github.com/hneemann/Digital/releases/latest/download/Digital.zip"
DIGITAL_JAR = "Digital.jar"
DIGITAL_ZIP = "Digital"
DIGITAL_PATH = Path(__file__).parent / DIGITAL_ZIP / DIGITAL_JAR
MAIN_FILE = Path(__file__).parent.parent / "src" / "main.dig"


def download_digital() -> None:
    """Download the jar file for Digital"""
    if DIGITAL_PATH.is_file():
        return

    print("Downloading Digital...")
    filehandle, _ = urllib.urlretrieve(DIGITAL_URL)

    with ZipFile(filehandle, "r") as zip_file:
        jar_path = str(Path(DIGITAL_ZIP) / DIGITAL_JAR)
        assert jar_path in zip_file.namelist()

        zip_file.extract(jar_path, Path(__file__).parent)


def main() -> None:
    """Run the tests on the simulator"""
    download_digital()

    print("Starting Digital...")
    with subprocess.Popen(
        ["java", "-jar", str(DIGITAL_PATH.resolve()), str(MAIN_FILE.resolve())],
        stdout=-1,
        stderr=-1,
    ) as digital_proc:
        time.sleep(2)
        tester = SimulatorTester()

        success = run_tests(tester)

        print("Stopping Digital")
        digital_proc.kill()

        if not success:
            sys.exit(1)


if __name__ == "__main__":
    main()
