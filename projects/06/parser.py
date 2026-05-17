"""Parser module for the Hack assembler.

Reads an assembly program (as an iterable of lines) and exposes one
instruction at a time, hiding whitespace and comments from the caller.
"""


class Parser:
    def __init__(self, lines):
        # `lines` is anything iterable that yields lines — a file object,
        # a list of strings, a generator, etc.
        #
        # Example usage:
        #   with open("Prog.asm") as f:
        #       parser = Parser(f)              # file object
        #
        #   parser = Parser(["@2\n", "D=A\n"])  # list of strings (e.g. in a test)
        self._iter = iter(lines)
        try:
            self._next_line = next(self._iter)
        except StopIteration:
            self._next_line = None
        self.current_instruction = None

    def has_more_lines(self):
        return self._next_line is not None

    def advance(self):
        while self._next_line is not None:
            line = self._next_line
            try:
                self._next_line = next(self._iter)
            except StopIteration:
                self._next_line = None
            instruction = line.split("//", 1)[0].strip()
            if instruction:
                self.current_instruction = instruction
                return
        self.current_instruction = None

    def instruction_type(self):
        if self.current_instruction.startswith("@"):
            return "A"
        if self.current_instruction.startswith("("):
            return "L"
        return "C"

    def symbol(self):
        if self.current_instruction.startswith("("):
            return self.current_instruction[1:-1]
        return self.current_instruction[1:]

    def dest(self):
        if "=" in self.current_instruction:
            return self.current_instruction.split("=", 1)[0]
        return ""

    def comp(self):
        result = self.current_instruction
        if "=" in result:
            result = result.split("=", 1)[1]
        if ";" in result:
            result = result.split(";", 1)[0]
        return result

    def jump(self):
        if ";" in self.current_instruction:
            return self.current_instruction.split(";", 1)[1]
        return ""
