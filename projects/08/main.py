"""Translates a VM file, or a directory of them, into a Hack assembly file."""

import sys
from pathlib import Path

from code_writer import CodeWriter
from parser import (
    C_ARITHMETIC, C_CALL, C_FUNCTION, C_GOTO, C_IF, C_LABEL, C_POP, C_PUSH,
    C_RETURN, Parser,
)


def translate(parser, writer):
    while parser.has_more_lines():
        parser.advance()
        command_type = parser.command_type()
        if command_type == C_ARITHMETIC:
            writer.write_arithmetic(parser.arg1())
        elif command_type == C_PUSH:
            writer.write_push(parser.arg1(), parser.arg2())
        elif command_type == C_POP:
            writer.write_pop(parser.arg1(), parser.arg2())
        elif command_type == C_LABEL:
            writer.write_label(parser.arg1())
        elif command_type == C_GOTO:
            writer.write_goto(parser.arg1())
        elif command_type == C_IF:
            writer.write_if(parser.arg1())
        elif command_type == C_FUNCTION:
            writer.write_function(parser.arg1(), parser.arg2())
        elif command_type == C_CALL:
            writer.write_call(parser.arg1(), parser.arg2())
        elif command_type == C_RETURN:
            writer.write_return()


input_path = Path(sys.argv[1]).resolve()
is_program = input_path.is_dir()
if is_program:
    vm_paths = sorted(input_path.glob("*.vm"))
    output_path = input_path / f"{input_path.name}.asm"
else:
    vm_paths = [input_path]
    output_path = input_path.with_suffix(".asm")

with open(output_path, "w") as f_out:
    writer = CodeWriter(f_out)
    if is_program:
        writer.write_bootstrap()
    for vm_path in vm_paths:
        with open(vm_path) as f_in:
            parser = Parser(f_in)
        writer.set_file_name(vm_path.stem)
        translate(parser, writer)
    writer.write_end()
