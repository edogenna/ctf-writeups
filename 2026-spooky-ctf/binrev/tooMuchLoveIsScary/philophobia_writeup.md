# SpookyCTF 2026 - Philophobia Writeup

## Challenge Description

**Category:** Bin/Rev

For this challenge, we are provided with an ELF executable named `philophobia`. The name itself (the fear of love) hints at a romantic or poetic theme. Our goal is to analyze the binary, bypass its initial checks, and decrypt the hidden flag.

## Reverse Engineering and Interaction

When running or analyzing `philophobia` in a disassembler like Ghidra, we can spot two distinct phases to this challenge:

### 1. The Initial Check
The binary starts by printing an output that ends with a line of spaces and a star (`              *              \n`). 
It then expects some specific inputs:
1. Two integers. In our testing, sending `0` and `1` (separated by a space) satisfies the requirement and sets up the buffer correctly.
2. A specific string payload. Based on the binary's checks (and keeping with the poetic theme), it expects the famous Shakespearean line: `Shall I compare thee`.

Our script automates this interaction using `pwntools`, sending the variables $x$ and $y$ as `0 1`, followed by `b'A' * x` concatenated with `Shall I compare thee`. Since $x = 0$, we simply send the quote.

### 2. Extracting and Decrypting the Flag
During static analysis, we also uncover a hardcoded encrypted array of bytes stored as 64-bit integers in Little Endian format. The bytes extracted from memory (omitting the trailing null bytes) are:

```
292a353531232137
6e233869056b0534
69693e052e6a056b
6a2c690537232969
6b3c27
```

This looks like a ciphertext $C$ that has been encrypted using a simple single-byte XOR key $K$.

## Cryptanalysis and Brute-force

Since the encryption is a single-byte XOR, the key space is incredibly small: $2^8 = 256$ possible keys. We don't even need to reverse the exact key generation function; we can just brute-force it.

Let $C_i$ be the $i$-th byte of the ciphertext, $P_i$ be the $i$-th byte of the plaintext flag, and $K$ be the unknown 8-bit key. The decryption function is:

$$
P_i = C_i \oplus K
$$

To find the correct key, we can iterate through all values from $0$ to $255$. For each key, we decrypt the ciphertext and check if the resulting plaintext consists entirely of printable ASCII characters (where the ASCII value is between $32$ and $126$). 

## Solution Script

The full solution is available in the `solve_3.py` script. The script is divided into two parts:
1. It optionally connects to the local process or GDB, bypassing the initial prompt by sending `0 1` and `Shall I compare thee`.
2. It runs the offline XOR brute-force algorithm on the extracted hex values, filtering the output to reveal the readable flag. 

By running the script, the brute-force quickly outputs the correct key and the decrypted flag!