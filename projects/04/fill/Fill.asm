// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.


(LOOP)
@KBD
M=0
@KBD
D=M

@FILL
D;JNE
@CLEAR
D;JEQ

(CLEAR)
@counter
M=0
(CLEARLOOP)
@counter
D=M
@10
D=D-A
@CLEARLOOPEND
D;JEQ

@counter
D=M
@SCREEN
A=A+D
M=0

@counter
M=M+1

@CLEARLOOP
0;JMP
(CLEARLOOPEND)
@LOOP
0;JMP

(FILL)

@counter
M=0

(FILLLOOP)

@counter
D=M
@10
D=D-A
@FILLLOOPEND
D;JEQ

@counter
D=M
@SCREEN
A=A+D
M=-1

@counter
M=M+1

@FILLLOOP
0;JMP
(FILLLOOPEND)

@LOOP
0;JMP
