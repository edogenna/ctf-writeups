# SpookyCTF - ELF Golfing / Quine Writeup

## Challenge Description

The goal of this challenge is to send an extremely small ("golfed") ELF executable to the server. From the expected interaction, it is clear that the server wants a minimal executable capable of acting as a *Quine*—meaning it must print its own code (its raw bytes) to standard output.

To solve the challenge, we had to manually craft a valid ELF file of exactly **112 bytes**, fitting the shellcode inside the unnecessary fields of the ELF Header and the Program Header.

## Analysis and Strategy (ELF Golfing)

Standard ELF files have many fields that the Linux kernel either ignores or does not strictly validate during memory loading. By exploiting this tolerance, we can:

1. **Overlap Headers:** Start the *Program Header* before the natural end of the *ELF Header*.

2. **Hide Shellcode:** Insert assembly instructions into non-critical fields (such as header padding, `p_paddr`, or other variables not essential for execution).

In our case, we split the shellcode into three separate "Slots" connected by relative jumps (`jmp`).

### ELF Structure and Shellcode Slots

The entry point was set to `0x400008` (byte 8 of our file).

**Slot A (Offset 8-15): Syscall Write Setup**
This slot exploits the space available in the ELF header padding.

```assembly
push 1      ; fd = 1 (stdout)
pop rdi
push 1      ; sys_write
pop rax
jmp +24     ; jump to Slot B (offset 40)
```

**The Overlap Trick**
At offset 32, we set `e_phoff = 0x38` (56 in decimal). This makes the *Program Header* start at offset 56, effectively overlapping and overwriting parts of the ELF Header.

* The `p_type` field of the Program Header (set to `PT_LOAD = 1`) perfectly overwrites `e_phnum` (which must be >= 1).
* The `p_flags` field (set to `R|X = 5`) overwrites `e_shnum` (which the kernel ignores for execution).

**Slot B (Offset 40-51): Executing the Write**
This slot is squeezed in just before the Program Header begins.

```assembly
mov esi, 0x400000  ; buffer = start of the ELF in memory
push 112           ; size = 112 bytes
pop rdx
syscall            ; executes sys_write(1, 0x400000, 112)
jmp +28            ; jump to Slot C (offset 80)
```

**Slot C (Offset 80-87): Clean Exit (Syscall Exit)**
This slot is hidden inside the `p_paddr` field of the Program Header. This field is completely obsolete and ignored by modern Linux kernels.

```assembly
xor edi, edi       ; exit code = 0
push 60            ; sys_exit
pop rax
syscall
nop
```

## Solution

The Python script packs all these bytes into a precise 112-byte array. Then, it performs the following steps:

1. Connects to the host `3.129.162.36` on port `31903`.
2. Declares the size of the payload by sending the command `SIZE 112\n`.
3. Sends the raw bytes of our golfed ELF.

For the complete implementation and payload delivery logic, please refer to the `solve.py` file included in this repository. Running the script will execute our file on the server, verify that it prints exactly its original 112 bytes, and reward us with the flag!