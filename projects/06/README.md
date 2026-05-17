# Project 06 — Assembler

A Python implementation of the Hack assembler. Translates Hack assembly
(`.asm`) into Hack binary machine code (`.hack`) using a two-pass approach:
pass one collects labels into the symbol table, pass two resolves symbols
and emits binary.

## Modules

- `main.py` — entrypoint and pass coordinator
- `parser.py` — strips comments/whitespace, classifies and parses instructions
- `code.py` — translates `dest`, `comp`, and `jump` mnemonics to bits
- `symbol_table.py` — symbol table with predefined symbols, labels, and variables

## Usage

    python main.py programs/Max.asm

Produces `programs/Max.hack` next to the input file.

## Programs

- `Add.asm` — adds 2 + 3, stores result in R0
- `Max.asm`, `MaxL.asm` — max of R0 and R1, stores in R2 (with/without labels)
- `Rect.asm`, `RectL.asm` — draws a rectangle on the screen
- `Pong.asm`, `PongL.asm` — the Pong game
