Python Computer Architecture Exercise - Readme
- Nate Tufts - bigbowlofnate@gmail.com


Summary: Created a very simple example of computer processor in Python. It uses a register, isa, alu, cache, main memory, and a set of instructions (written in binary, not assembly). The main function of this exercise was to allow the addition, subtraction, multiplication, or division of two numbers at a time. It follows processor protocol where everything must be loaded into the register to be operated on. Not even close to being fully tested.

Directions: Python 3 program. Drop all these files in the same folder and use ISA.PY to run the program. There is no user input, there are a set of instructions that load some binary numbers into memory, they are then extracted from memory and operated on. The results can be hard to wade through, but I isolated the actual output answers which tell what arithmetic was used, the values of the two numbers operated on, as well as the final answer.


Files:

isa.py - Starting file. hub of the program, imports all the other files.   

alu.py - Arithmetic, gates, and any other functions that alter the binary numbers.

memory.py - contains the memory, cache, and main memory parent and child classes.

register.py - built like memory, but saved in its own file for clarity.

instructions.py - a file of binary instructions that are called into isa.py and parsed into single 32 bit lines.