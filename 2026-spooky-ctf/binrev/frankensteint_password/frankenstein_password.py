from pwn import *

COMMANDS = """
  b *0x40132A
  c
"""

context.arch = "amd64"

if args.GDB:
  c = gdb.debug("./frankenstein", gdbscript=COMMANDS)
else:
  c = process("./frankenstein")


c.recvuntil(b"Activation phrase: ")

def solve():
  # I 14 byte estratti dall'indirizzo 0x402010 (convertiti da little-endian)
  target_bytes = [
      0x2a, 0x24, 0x2a, 0x29, 0x43, 0x37, 0x45, 0x50, 
      0x5c, 0x5d, 0x65, 0x72, 0x74, 0x6f
  ]
  
  flag = ""
  for i in range(14):
      # Sottraiamo 11 e 7*i dal byte target simulando l'overflow a 8-bit
      val = (target_bytes[i] - 11 - (7 * i)) & 0xFF
      
      # Riapplichiamo lo XOR con 0x5D
      char_val = val ^ 0x5D
      
      # Aggiungiamo il carattere alla flag
      flag += chr(char_val)

  print(f"La flag per ottenere return 1 è: {flag}")
  return flag

flag = solve()
c.sendline(flag.encode())

c.interactive()