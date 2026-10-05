"""Translates VM commands into Hack assembly."""

_BINARY_OPS = {
    "add": "M=D+M",
    "sub": "M=M-D",
    "and": "M=D&M",
    "or": "M=D|M",
}

_UNARY_OPS = {
    "neg": "M=-M",
    "not": "M=!M",
}

_ORDERINGS = {
    "gt": ("0", "-1", "JGT"),
    "lt": ("-1", "0", "JLT"),
}

_BASES = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
}

_TEMP_BASE = 5

_POINTERS = ("THIS", "THAT")

_PUSH_D = ["@SP", "M=M+1", "A=M-1", "M=D"]


def _eq_lines(n):
    return [
        "@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "M=-1",
        f"@END_{n}", "D;JEQ",
        "@SP", "A=M-1", "M=0",
        f"(END_{n})",
    ]


def _ordering_lines(n, x_below, x_above, same_sign_jump):
    return [
        "@SP", "AM=M-1", "D=M",
        f"@YNEG_{n}", "D;JLT",
        "@SP", "A=M-1", "D=M", f"M={x_below}",
        f"@END_{n}", "D;JLT",
        f"@SAME_{n}", "0;JMP",
        f"(YNEG_{n})",
        "@SP", "A=M-1", "D=M", f"M={x_above}",
        f"@END_{n}", "D;JGE",
        f"(SAME_{n})",
        "@SP", "A=M", "D=D-M",
        "@SP", "A=M-1", "M=-1",
        f"@END_{n}", f"D;{same_sign_jump}",
        "@SP", "A=M-1", "M=0",
        f"(END_{n})",
    ]


class CodeWriter:
    def __init__(self, out, file_name):
        self._out = out
        self._file_name = file_name
        self._label_count = 0

    def write_arithmetic(self, command):
        if command in _BINARY_OPS:
            lines = ["@SP", "AM=M-1", "D=M", "A=A-1", _BINARY_OPS[command]]
        elif command in _UNARY_OPS:
            lines = ["@SP", "A=M-1", _UNARY_OPS[command]]
        elif command == "eq":
            lines = _eq_lines(self._label_count)
            self._label_count += 1
        else:
            lines = _ordering_lines(self._label_count, *_ORDERINGS[command])
            self._label_count += 1
        self._out.write("\n".join(lines) + "\n")

    def write_push(self, segment, index):
        if segment == "constant":
            lines = [f"@{index}", "D=A"]
        elif segment == "temp":
            lines = [f"@{_TEMP_BASE + index}", "D=M"]
        elif segment == "pointer":
            lines = [f"@{_POINTERS[index]}", "D=M"]
        elif segment == "static":
            lines = [f"@{self._file_name}.{index}", "D=M"]
        else:
            lines = [f"@{_BASES[segment]}", "D=M", f"@{index}", "A=D+A", "D=M"]
        self._out.write("\n".join(lines + _PUSH_D) + "\n")

    def write_pop(self, segment, index):
        if segment == "temp":
            lines = ["@SP", "AM=M-1", "D=M", f"@{_TEMP_BASE + index}", "M=D"]
        elif segment == "pointer":
            lines = ["@SP", "AM=M-1", "D=M", f"@{_POINTERS[index]}", "M=D"]
        elif segment == "static":
            lines = ["@SP", "AM=M-1", "D=M", f"@{self._file_name}.{index}", "M=D"]
        else:
            lines = [
                f"@{_BASES[segment]}", "D=M", f"@{index}", "D=D+A",
                "@R13", "M=D",
                "@SP", "AM=M-1", "D=M",
                "@R13", "A=M", "M=D",
            ]
        self._out.write("\n".join(lines) + "\n")

    def write_end(self):
        self._out.write("\n".join([
            "(END)",
            "@END",
            "0;JMP",
        ]) + "\n")
