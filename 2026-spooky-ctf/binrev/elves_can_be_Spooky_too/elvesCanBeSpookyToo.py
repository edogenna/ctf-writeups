import socket
import time

def solve():
    # Costruiamo il Quine ELF golfato: sovrapposizione perfetta in 112 byte!
    elf = bytearray()
    
    # 0-7: Magic e_ident
    elf += b"\x7FELF\x02\x01\x01\x00"
    
    # 8-15: Slot A - Shellcode 1
    # push 1; pop rdi; push 1; pop rax; jmp +24 (salta all'offset 40)
    elf += b"\x6a\x01\x5f\x6a\x01\x58\xeb\x18"
    
    # 16-23: e_type (02 00), e_machine (3E 00), e_version (01 00 00 00)
    elf += b"\x02\x00\x3E\x00\x01\x00\x00\x00"
    
    # 24-31: e_entry (0x400008, punta allo Slot A)
    elf += b"\x08\x00\x40\x00\x00\x00\x00\x00"
    
    # 32-39: e_phoff (impostato a 56 / 0x38) - IL TRUCCO È QUI!
    elf += b"\x38\x00\x00\x00\x00\x00\x00\x00"
    
    # 40-51: Slot B - Shellcode 2 (12 byte)
    # mov esi, 0x400000; push 112; pop rdx; syscall; jmp +28 (salta all'offset 80)
    elf += b"\xbe\x00\x00\x40\x00\x6a\x70\x5a\x0f\x05\xeb\x1c"
    
    # 52-55: e_ehsize (64), e_phentsize (56) - Obbligatori per il kernel
    elf += b"\x40\x00\x38\x00"
    
    # --- INIZIO PROGRAM HEADER (Offset 56) ---
    
    # 56-59: p_type (PT_LOAD = 1) -> Sovrascrive e_phnum (1) e e_shentsize (0)
    # Perfetto: e_phnum deve essere >= 1!
    elf += b"\x01\x00\x00\x00"
    
    # 60-63: p_flags (R|X = 5) -> Sovrascrive e_shnum (5) e e_shstrndx (0)
    # Perfetto: al kernel non interessano le sezioni (e_shnum)!
    elf += b"\x05\x00\x00\x00"
    
    # 64-71: p_offset (0)
    elf += b"\x00\x00\x00\x00\x00\x00\x00\x00"
    
    # 72-79: p_vaddr (0x400000)
    elf += b"\x00\x00\x40\x00\x00\x00\x00\x00"
    
    # 80-87: Slot C - Shellcode 3 (sfrutta p_paddr, obsoleto)
    # xor edi, edi; push 60; pop rax; syscall; nop
    elf += b"\x31\xff\x6a\x3c\x58\x0f\x05\x90"
    
    # 88-95: p_filesz (112)
    elf += b"\x70\x00\x00\x00\x00\x00\x00\x00"
    
    # 96-103: p_memsz (112)
    elf += b"\x70\x00\x00\x00\x00\x00\x00\x00"
    
    # 104-111: p_align (0)
    elf += b"\x00\x00\x00\x00\x00\x00\x00\x00"
    
    # --- FINE FILE ---
    assert len(elf) == 112, "L'ELF generato non è di 112 byte!"
    
    # Setup connessione
    host = '3.129.162.36'
    port = 31903
    
    print(f"[*] Connessione a {host}:{port}...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    time.sleep(0.5)
    banner = s.recv(1024).decode(errors='ignore')
    print("[*] Banner ricevuto:\n" + banner.strip())
    
    # Inviamo la size esatta (112 byte) seguita da \n
    print("[*] Segnalo la dimensione (112)...")
    s.sendall(b"SIZE 112\n")
    time.sleep(0.5)
    
    # Spara il Payload "Quine"
    print("[*] Invio dell'eseguibile ELF golfato...")
    s.sendall(elf)
    
    time.sleep(1)
    response = s.recv(1024).decode(errors='ignore')
    print("[*] Risposta dal server:\n\n" + response.strip())
    s.close()

if __name__ == "__main__":
    solve()