out_data = bytearray()

with open('serial-capture.log', 'r') as f:
    reading_payload = False
    current_block = bytearray()
    
    for line in f:
        if line.startswith('>'):
            reading_payload = True
            current_block = bytearray()
        elif line.startswith('<') or line.startswith('--'):
            if reading_payload and len(current_block) > 3:
                # Scarta i 3 byte di header (es. 01 01 fe) e tiene il payload
                out_data.extend(current_block[3:131])
            reading_payload = False
        elif reading_payload:
            # Estrae la parte esadecimale ignorando la colonna ASCII a destra
            # I byte hex arrivano fino al carattere 49 della stringa
            hex_part = line[1:49]
            for byte_str in hex_part.split():
                current_block.append(int(byte_str, 16))

with open('challenge.jpg', 'wb') as out_file:
    out_file.write(out_data)

print("Immagine JPEG estratta con successo!")