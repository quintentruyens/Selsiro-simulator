"""
Provides SimulatorTester, the implementation of the Tester interface for the simulator
implementation of the CPU in Digital
"""

import socket
from typing import Optional
from pathlib import Path
import time
import json
from tests.tester import Tester

PROGRAM_FILE = Path(__file__).parent / "program.bin"
DIGITAL_PORT = 41114

MEMORY_SIZE = 4 << 24


class SimulatorTester(Tester):
    "Allows testing of the Digital simulator implementation"

    def __init__(self) -> None:
        super().__init__()
        self.program_counter = 0
        self.registers = [0] * 32

    def update_registers(self) -> None:
        """Update the registers property"""
        response = send_request("measure")
        assert response is not None
        measurements = json.loads(response)
        for i in range(32):
            self.registers[i] = int(measurements[f"r{i}"])

    def start(self, program: bytes) -> None:
        with PROGRAM_FILE.open("wb") as file:
            file.write(program)
            file.flush()

        assert send_request("debug", str(PROGRAM_FILE.resolve())) is None

        time.sleep(2)
        self.update_registers()

    def stop(self) -> None:
        assert send_request("stop") is None
        time.sleep(2)

    def clock(self) -> None:
        response = send_request("step")
        assert response is not None
        self.program_counter = int(response, 16)
        self.update_registers()

    def get_pc(self) -> int:
        return self.program_counter

    def get_register(self, reg_num: int) -> int:
        return self.registers[reg_num]

    def read_memory(self, address: int) -> int:
        raise NotImplementedError()


def send_request(request: str, args: Optional[str] = None) -> Optional[str]:
    """Send the given request to the currently running Digital process"""
    with socket.create_connection(("localhost", DIGITAL_PORT), timeout=10) as sock:

        message = request + ("" if args is None else (":" + args))
        encoded = message.encode(encoding="UTF-8")
        utfmsg = len(encoded).to_bytes(2, byteorder="big", signed=False) + encoded
        sock.sendall(utfmsg)

        response_length_bytes = bytes()
        while len(response_length_bytes) != 2:
            response_length_bytes += sock.recv(2 - len(response_length_bytes))

        response_length = int.from_bytes(
            response_length_bytes, byteorder="big", signed=False
        )
        response = sock.recv(response_length).decode(encoding="UTF-8")

        if response.startswith("ok:"):
            return response[3:]
        if response == "ok":
            return None
        print(f"Error during command '{message}': '{response}'")
        raise AssertionError(response)
