"""
Generate the control ROM for the simulator
"""

import argparse
from pathlib import Path
from typing import BinaryIO, Iterator
from enum import IntEnum, IntFlag, unique

parser = argparse.ArgumentParser(description="A script for generating the ROM")

parser.add_argument(
    "--output",
    "-o",
    help="The output file for this script",
    default=Path(__file__).parent / "control.bin",
    type=Path,
)


@unique
class Opcode(IntEnum):
    """Definition of the possible opcodes"""

    LOAD = 0b0000011
    LOAD_FP = 0b0000111
    MISC_MEM = 0b0001111
    OP_IMM = 0b0010011
    AUIPC = 0b0010111
    OP_IMM_32 = 0b0011011
    STORE = 0b0100011
    STORE_FP = 0b0100111
    AMO = 0b0101111
    OP = 0b0110011
    LUI = 0b0110111
    OP_32 = 0b0111011
    MADD = 0b1000011
    MSUB = 0b1000111
    NMSUB = 0b1001011
    NMADD = 0b1001111
    OP_FP = 0b1010011
    BRANCH = 0b1100011
    JALR = 0b1100111
    JAL = 0b1101111
    SYSTEM = 0b1110011
    OPCODE_MAX = 0b1111111


class Funct3(IntEnum):
    """Definitions of funct3 values"""

    ADD = 0b000
    SLL = 0b001
    SLT = 0b010
    STLU = 0b011
    XOR = 0b100
    SR = 0b101
    OR = 0b110
    AND = 0b111
    FUNC3_MAX = 0b111


class Funct7(IntEnum):
    """Definitions of funct7 values"""

    FUNCT7_MAX = 0b1111111


class Ctrl(IntFlag):
    """Definitions of the bits in the control word and some useful combinations of them"""

    STR_REG = 1 << 0
    ILLEGAL_INSTR = 1 << 1

    ADDI = STR_REG


# Width of a control word in bits
CTRL_WIDTH = 2


def gen_control() -> Iterator[Ctrl]:
    """Produces the control words for every address in the control ROM"""
    for opcode in range(Opcode.OPCODE_MAX + 1):
        for funct3 in range(Funct3.FUNC3_MAX + 1):
            for _funct7 in range(Funct7.FUNCT7_MAX + 1):
                if opcode == Opcode.OP_IMM:
                    if funct3 == Funct3.ADD:
                        yield Ctrl.ADDI
                    else:
                        yield Ctrl.ILLEGAL_INSTR
                else:
                    yield Ctrl.ILLEGAL_INSTR


def write_control(file: BinaryIO):
    """Write the control ROM to the given file"""
    for ctrl in gen_control():
        file.write(ctrl.to_bytes((CTRL_WIDTH + 7) // 8, "little"))


def main():
    """Generate the control ROM"""
    args = parser.parse_args()
    with args.output.open("wb") as file:
        write_control(file)


if __name__ == "__main__":
    main()
