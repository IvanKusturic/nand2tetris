// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

(KBD_CHECK)
    @i
    M=0
    @KBD
    D=M
    @FILL_BLACK
    D;JNE

(FILL_WHITE)

    @SCREEN
    D=A
    @i
    D=D+M
    A=D
    M=0
    @i
    M=M+1
    @8192
    D=A
    @i
    D=M-D
    @FILL_WHITE
    D;JLT
    @KBD_CHECK
    0;JMP

(FILL_BLACK)

    @SCREEN
    D=A
    @i
    D=D+M
    A=D
    M=-1
    @i
    M=M+1
    @8192
    D=A
    @i
    D=M-D
    @FILL_BLACK
    D;JLT
    @KBD_CHECK
    0;JMP