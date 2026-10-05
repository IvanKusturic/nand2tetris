# Project 07 — VM Translator I: Stack Arithmetic

A Python implementation of the first half of the VM translator. Translates a
VM program (`.vm`) into Hack assembly (`.asm`): the nine arithmetic and
logical commands, and `push`/`pop` across all eight memory segments.

## Modules

- `main.py` — entrypoint; reads the input and dispatches each command to the writer
- `parser.py` — strips comments/whitespace, splits each command into fields
- `code_writer.py` — emits the Hack assembly for each command

## Usage

    python main.py programs/SimpleAdd/SimpleAdd.vm

Produces `programs/SimpleAdd/SimpleAdd.asm` next to the input file. To test,
load it in the CPU Emulator with the `.tst` script from the same folder.

## Programs

- `SimpleAdd` — pushes and adds two constants
- `StackTest` — all nine arithmetic and logical commands
- `BasicTest` — push/pop on `local`, `argument`, `this`, `that`, `temp`
- `PointerTest` — `pointer`, and `this`/`that` through it
- `StaticTest` — `static`
