Description:
This project is a GUI-based custom code interpreter built using Python's tkinter. The program allows users to enter and execute a simplified, domain-specific scripting language that mimics basic programming structures such as conditional execution, loops, assignments, and output display.

Key Features:
Custom Scripting Syntax:
Code must start with India
Supports variable assignments
Conditional statements: when, otherwise when, otherwise
Looping: repeat(n)
Output command: say "message" or say expression

Output Display:
Main output window for interpreted message.
Separate window for generated Three Address Code (TAC)

Progress Bar:
Simulated progress shown while interpreting code

Usage:
Run the script using Python 3.
Enter your custom code into the text area.
Click the "Run Code" button to execute.
The program will display output and the corresponding TAC in two separate windows.

Dependencies:
Python standard libraries: tkinter, re, time, keyword

Example Input Code:
India
x = 5
y = 10
say "Start"
when x < y {
  say "x is less than y"
}
otherwise {
  say "x is not less than y"
}
repeat(3) {
  say "Hello"
}


Note:
Make sure the first line of the input is India or the interpreter will reject it.
The interpreter is sensitive to syntax. Follow the structure as demonstrated in the example.

Author: Dhairya Gohil
Date: 14th May 2025