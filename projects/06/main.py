"""Main module for the Hack assembler (v2: with symbols).

Coordinator: owns file I/O, runs two passes — pass 1 collects labels
into the symbol table, pass 2 translates instructions to binary,
resolving symbols and allocating variable addresses.
"""

import sys
from pathlib import Path

import code
from parser import Parser
from symbol_table import SymbolTable


input_path = Path(sys.argv[1])
output_path = input_path.with_suffix(".hack")

table = SymbolTable()

with open(input_path) as f_in:
    p = Parser(f_in)
    rom_line = 0
    while p.has_more_lines():
        p.advance()
        if p.instruction_type() == "L":
            table.add_entry(p.symbol(), rom_line)
        else:
            rom_line += 1

with open(input_path) as f_in, open(output_path, "w") as f_out:
    p = Parser(f_in)
    next_var = 16
    while p.has_more_lines():
        p.advance()
        t = p.instruction_type()
        if t == "A":
            s = p.symbol()
            if s.isdigit():
                address = int(s)
            elif table.contains(s):
                address = table.get_address(s)
            else:
                table.add_entry(s, next_var)
                address = next_var
                next_var += 1
            line = "0" + f"{address:015b}"
            f_out.write(line + "\n")
        elif t == "C":
            line = "111" + code.comp(p.comp()) + code.dest(p.dest()) + code.jump(p.jump())
            f_out.write(line + "\n")
        # L: skip — not emitted
