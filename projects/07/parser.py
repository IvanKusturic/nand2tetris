"""Reads a VM program and exposes one command at a time."""

C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"


class Parser:
    def __init__(self, lines):
        split_lines = (line.split("//", 1)[0].split() for line in lines)
        self._commands = [words for words in split_lines if words]
        self._index = -1

    def has_more_lines(self):
        return self._index + 1 < len(self._commands)

    def advance(self):
        self._index += 1

    def command_type(self):
        first_word = self._commands[self._index][0]
        if first_word == "push":
            return C_PUSH
        if first_word == "pop":
            return C_POP
        return C_ARITHMETIC

    def arg1(self):
        words = self._commands[self._index]
        if self.command_type() == C_ARITHMETIC:
            return words[0]
        return words[1]

    def arg2(self):
        return int(self._commands[self._index][2])
