# SpookyCTF 2026 - Binary Writeup

## Challenge Description

**Category:** Reverse Engineering

In this challenge, we are given a compiled Java class file named `binary.class`. Running the program without arguments prints a usage message: `Usage: java binary <flag>`. Our objective is to reverse engineer the compiled byte code to understand the flag validation logic and extract the correct 34-character flag.

## Reverse Engineering and Analysis

The first step is to decompile the `binary.class` file to readable Java source code. This can be done using standard decompilers like CFR, Procyon, or online Java decompilers. The resulting decompiled code (which we saved as `binary.java`) reveals the core logic.

The `main` function simply passes our command-line argument to a `check` method. 
Looking into `check(String var0)`, we observe the following constraints:
1. The length of the string must be exactly $34$ characters.
2. The string undergoes a massive nested `if` statement block. 

Inside this block, the program takes the ASCII integer value of each character (e.g., `var0.charAt(0)`) and applies various arithmetic and bitwise operations—specifically additions, subtractions, and bitwise XORs ($\oplus$)—comparing the results to hardcoded target values.

For example, the checks for the first four characters look like this:
*   Character 0: `(31 ^ c[0]) + 7 == 115`
*   Character 1: `(73 - c[1]) ^ 11 == -46`
*   Character 2: `(c[2] + 5) ^ 22 == 98`
*   Character 3: `19 - c[3] + 51 == -41`

## Solution Strategy: Z3 Theorem Prover

While we could algebraically reverse each equation by hand, this is tedious and prone to human error, especially given the sheer number of equations and the risk of integer underflow/overflow. 

Instead, the optimal approach is to use an SMT (Satisfiability Modulo Theories) solver like **Z3**. Z3 allows us to define the unknown variables, apply the constraints exactly as they appear in the decompiled Java code, and let the solver find the input that satisfies all conditions.

### Z3 Implementation Details

We translate the Java logic into Python using the `z3-solver` library:

1. **Variables:** We define 34 variables representing the characters of the flag. Since Java uses 32-bit signed integers for these arithmetic operations, we model our variables as 32-bit BitVectors (`BitVec(..., 32)`).
2. **ASCII Constraints:** To ensure the solver gives us a readable string, we restrict the domain of each variable to printable ASCII characters ($32 \le x \le 126$).
3. **Translating the Checks:** We transcribe the equations block by block. We must be careful with operator precedence: in Python, the bitwise XOR (`^`) has lower precedence than addition (`+`) and subtraction (`-`). To ensure our Python script accurately models the Java checks, we explicitly group the operations using parentheses.
4. **Evaluation:** We instruct Z3 to check for satisfiability (`solver.check()`). If a solution is found, we evaluate the model, convert the 32-bit integers back into characters, and concatenate them to reveal the flag.

## Solution Script

The complete Python Z3 script can be found in the `solve_4.py` file included in this repository. Running the script will instantly solve the system of equations and print the winning flag, completely bypassing the need to manually reverse 34 separate math equations!