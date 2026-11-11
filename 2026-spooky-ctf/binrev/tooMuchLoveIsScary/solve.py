from pwn import *

COMMANDS = """
  brva 0x14B9
  c
"""

context.arch = "amd64"

if args.GDB:
  c = gdb.debug("./philophobia", gdbscript=COMMANDS)
elif args.LOCAL:
  c = process("./philophobia")

  c.recvuntil(b"              *              \n")

  #send two numbers for example 0 and 1
  x = 0
  y = 1
  payload = str(x) + " " + str(y)
  c.sendline(payload)

  payload = b'A' * x
  payload += b'Shall I compare thee'
  c.sendline(payload)
  c.interactive()


# I dati estratti e convertiti in byte (Little Endian)
# Abbiamo rimosso i byte nulli finali che servono solo a fermare il for in C
cipher = bytes.fromhex(
    "292a353531232137"  # v4[0] = 0x3721233135352A29
    "6e233869056b0534"  # v4[1] = 0x34056B056938236E
    "69693e052e6a056b"  # v4[2] = 0x6B056A2E053E6969
    "6a2c690537232969"  # v4[3] = 0x6929233705692C6A
    "6b3c27"            # v5    = 0x000000273C6B
)

print("[*] Inizio brute-force dello XOR...")

# Proviamo tutte le possibili chiavi a 8 bit
for k in range(256):
    decrypted = ""
    for byte in cipher:
        decrypted += chr(byte ^ k)
    
    # Filtriamo l'output per stampare solo le stringhe che contengono
    # caratteri stampabili standard per ridurre il "rumore".
    if all(32 <= ord(c) <= 126 for c in decrypted):
        print(f"Key: {k} (0x{k:02x}) -> {decrypted}")