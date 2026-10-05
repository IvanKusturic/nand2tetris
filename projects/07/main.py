"""Translates a VM file into a Hack assembly file."""

import sys
from pathlib import Path

from code_writer import CodeWriter
from parser import C_ARITHMETIC, C_POP, C_PUSH, Parser

input_path = Path(sys.argv[1])
output_path = input_path.with_suffix(".asm")

with open(input_path) as f_in:
    parser = Parser(f_in)

with open(output_path, "w") as f_out:
    writer = CodeWriter(f_out, input_path.stem)
    while parser.has_more_lines():
        parser.advance()
        command_type = parser.command_type()
        if command_type == C_ARITHMETIC:
            writer.write_arithmetic(parser.arg1())
        elif command_type == C_PUSH:
            writer.write_push(parser.arg1(), parser.arg2())
        elif command_type == C_POP:
            writer.write_pop(parser.arg1(), parser.arg2())
    writer.write_end()
