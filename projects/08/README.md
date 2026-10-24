# Project 08 — VM Translator II: Program Control

A Python implementation of the complete VM translator. Extends Project 07 with
program flow (`label`, `goto`, `if-goto`) and function calls (`function`,
`call`, `return`), and translates a single `.vm` file or a whole directory of
them into one Hack assembly file.

## Modules

- `main.py` — entrypoint; collects the input files and dispatches each command to the writer
- `parser.py` — strips comments/whitespace, splits each command into fields
- `code_writer.py` — emits the Hack assembly for each command, and the bootstrap

## Usage

    python main.py programs/BasicLoop/BasicLoop.vm
    python main.py programs/FibonacciElement

A file produces `BasicLoop.asm` next to it. A directory is a whole program:
all its `.vm` files are translated into `FibonacciElement/FibonacciElement.asm`,
preceded by bootstrap code that sets `SP` to 256 and calls `Sys.init`. To test,
load the `.asm` in the CPU Emulator with the `.tst` script from the same folder.

## Programs

- `BasicLoop` — sums 1..n in a loop
- `FibonacciSeries` — writes the first n Fibonacci numbers to memory
- `SimpleFunction` — a function with local variables
- `NestedCall` — nested calls; checks that the caller's frame is restored
- `FibonacciElement` — recursive Fibonacci across two files
- `StaticsTest` — static variables kept separate per file
