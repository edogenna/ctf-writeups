# SpookyCTF 2026 - Frankenstein's Password Generator Writeup

## Challenge Description
**Category:** Bin/Rev
**Difficulty:** Medium

According to the provided `README.txt`, we are tasked with finding an "activation phrase" to start a password generator left behind by Dr. Frankenstein in an abandoned laboratory. The challenge provides a Linux x86-64 ELF executable named `frankenstein`. Our goal is to reverse engineer the binary to discover the correct input phrase that yields the flag.

## Reverse Engineering and Analysis
When running the `frankenstein` executable, it prompts the user with:
`Activation phrase: `

By loading the binary into a disassembler/decompiler (like Ghidra or IDA Pro) and analyzing the validation function (around address `0x40132A`, as hinted by the GDB breakpoint in the solver script), we can uncover the algorithm used to verify the user input.

The binary takes the user's input string, iterates through its characters, and performs a series of mathematical operations on each byte. The transformed bytes are then compared against a hardcoded array of 14 target bytes stored in the `.rodata` or `.data` section at memory address `0x402010`.

The target byte array found at `0x402010` is:
`0x2a, 0x24, 0x2a, 0x29, 0x43, 0x37, 0x45, 0x50, 0x5c, 0x5d, 0x65, 0x72, 0x74, 0x6f`

### The Encryption Algorithm
Let $c_i$ be the $i$-th character of our input, and $t_i$ be the $i$-th byte in the target array. 
Based on the provided solution script, the binary transforms our input using the following logic:
1. It applies an XOR operation on the input character with `0x5D`.
2. It adds `11` to the result.
3. It adds $7 \times i$ (where $i$ is the character's index).
4. All additions are constrained to an 8-bit space (modulo 256).

The forward operation looks like this:
$$ t_i = ( (c_i \oplus \text{0x5D}) + 11 + (7 \times i) ) \pmod{256} $$

## Reversing the Algorithm
To find the correct activation phrase, we need to reverse the operations applied by the binary to get back to the original $c_i$. We can do this by working backwards from the target bytes $t_i$:

1. Subtract $11$ and $7 \times i$ from the target byte $t_i$.
2. Apply a modulo $256$ (or bitwise AND with `0xFF`) to simulate 8-bit integer underflow/overflow.
3. XOR the result again with `0x5D` (since XOR is its own inverse).

The reversed formula is:
$$ c_i = ( (t_i - 11 - (7 \times i)) \pmod{256} ) \oplus \text{0x5D} $$

## Solution Script
We can automate this decryption process using Python and the `pwntools` library to directly interact with the binary. 

For the complete implementation, please refer to the `solve_2.py` file included in this repository. The script calculates the correct flag by applying the reverse formula to the 14 extracted bytes and then sends the generated activation phrase to the local process (or GDB instance) to successfully "wake the creature" and solve the challenge.