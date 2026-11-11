from z3 import *

# Inizializziamo il solver
solver = Solver()

# La flag è lunga 34 caratteri.
# Usiamo BitVec a 32 bit per simulare il comportamento degli int a 32 bit di Java
flag = [BitVec(f"c_{i}", 32) for i in range(34)]

# Aggiungiamo un vincolo generico per limitare la ricerca ai caratteri ASCII stampabili
for i in range(34):
    solver.add(flag[i] >= 32, flag[i] <= 126)

# Trascriviamo i controlli copiandoli quasi 1:1 dal codice Java
# Attenzione alle precedenze: in Python/Java le addizioni/sottrazioni 
# vengono valutate PRIMA dello XOR. Mettiamo le parentesi per sicurezza.

# Blocco 0
solver.add(((31 ^ flag[0]) + 7) == 115)
solver.add(((73 - flag[1]) ^ 11) == -46)
solver.add(((flag[2] + 5) ^ 22) == 98)
solver.add((19 - flag[3] + 51) == -41)

# Blocco 1
solver.add(((94 ^ flag[4]) + 13) == 66)
solver.add(((37 - flag[5]) ^ 23) == -69)
solver.add(((flag[6] + 17) ^ 12) == 128)
solver.add((3 - flag[7] + 83) == -15)

# Blocco 2
solver.add(((41 ^ flag[8]) + 29) == 124)
solver.add(((66 - flag[9]) ^ 9) == -44)
solver.add(((flag[10] + 21) ^ 9) == 142)
solver.add((15 - flag[11] + 55) == -25)

# Blocco 3
solver.add(((88 ^ flag[12]) + 27) == 69)
solver.add(((14 - flag[13]) ^ 31) == -74)
solver.add(((flag[14] + 7) ^ 79) == 50)
solver.add((25 - flag[15] + 33) == -43)

# Blocco 4
solver.add(((61 ^ flag[16]) + 11) == 90)
solver.add(((27 - flag[17]) ^ 17) == -71)
solver.add(((flag[18] + 13) ^ 48) == 66)
solver.add((25 - flag[19] + 88) == 13)

# Blocco 5
solver.add(((32 ^ flag[20]) + 9) == 136)
solver.add(((69 - flag[21]) ^ 28) == -57)
solver.add(((flag[22] + 12) ^ 13) == 96)
solver.add((31 - flag[23] + 50) == -37)

# Blocco 6
solver.add(((87 ^ flag[24]) + 15) == 69)
solver.add(((31 - flag[25]) ^ 34) == -62)
solver.add(((flag[26] + 18) ^ 68) == 23)
solver.add((37 - flag[27] + 12) == -5)

# Blocco 7
solver.add(((49 ^ flag[28]) + 21) == 27)
solver.add(((86 - flag[29]) ^ 5) == -15)
solver.add(((flag[30] + 24) ^ 30) == 105)
solver.add((8 - flag[31] + 67) == 18)

# Blocco 8
solver.add(((11 ^ flag[32]) + 27) == 85)
solver.add(((48 - flag[33]) ^ 11) == -72)

# Risolviamo
if solver.check() == sat:
    model = solver.model()
    # Estraiamo i valori in ordine, li convertiamo in char e li concateniamo
    risultato = "".join([chr(model[flag[i]].as_long()) for i in range(34)])
    print(f"Flag trovata: {risultato}")
else:
    print("Nessuna soluzione trovata. Controlla i vincoli.")