"""Functionality related to the downloading and running of Digital"""

from pathlib import Path
import urllib.request as urllib
from zipfile import ZipFile
import subprocess

DIGITAL_URL = "https://github.com/hneemann/Digital/releases/latest/download/Digital.zip"
DIGITAL_JAR = "Digital.jar"
DIGITAL_ZIP = "Digital"
DIGITAL_PATH = Path(__file__).parent / DIGITAL_ZIP / DIGITAL_JAR


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


def run_digital(dig_file: Path) -> subprocess.Popen[bytes]:
    """Runs an instance of Digital"""
    download_digital()
    return subprocess.Popen(
        ["java", "-jar", str(DIGITAL_PATH.resolve()), str(dig_file.resolve())],
        stdout=-1,
        stderr=-1,
    )


def run_digital_tests(dig_file: Path) -> bool:
    """Uses Digital to run the unit tests in the given file"""
    download_digital()
    # pylint: disable-next=subprocess-run-check
    result = subprocess.run(
        [
            "java",
            "-cp",
            str(DIGITAL_PATH.resolve()),
            "CLI",
            "test",
            "-circ",
            str(dig_file.resolve()),
        ],
    )

    return result.returncode == 0
