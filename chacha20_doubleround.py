print("Aufgabe 2.2")
def rotl32(v, c):
    """Führt eine bitweise Linksrotation für 32-Bit Integer durch."""
    return ((v << c) & 0xFFFFFFFF) | (v >> (32 - c))

def quarter_round(x, a, b, c, d):
    """Führt einen ChaCha20 Quarter Round auf den Indizes a, b, c, d im Array x aus."""
    x[a] = (x[a] + x[b]) & 0xFFFFFFFF
    x[d] = rotl32(x[d] ^ x[a], 16)
    
    x[c] = (x[c] + x[d]) & 0xFFFFFFFF
    x[b] = rotl32(x[b] ^ x[c], 12)
    
    x[a] = (x[a] + x[b]) & 0xFFFFFFFF
    x[d] = rotl32(x[d] ^ x[a], 8)
    
    x[c] = (x[c] + x[d]) & 0xFFFFFFFF
    x[b] = rotl32(x[b] ^ x[c], 7)

def double_round(state):
    """Führt eine ChaCha20 Double Round (Spalten, dann Diagonalen) aus."""
    #Spalten
    quarter_round(state, 0, 4,  8, 12)
    quarter_round(state, 1, 5,  9, 13)
    quarter_round(state, 2, 6, 10, 14)
    quarter_round(state, 3, 7, 11, 15)
    
    #Diagonalen
    quarter_round(state, 0, 5, 10, 15)
    quarter_round(state, 1, 6, 11, 12)
    quarter_round(state, 2, 7,  8, 13)
    quarter_round(state, 3, 4,  9, 14)

def print_state(state, title="State"):
    """Hilfsfunktion zur schönen Matrix-Ausgabe des Zustands."""
    print(f"--- {title} ---")
    for i in range(0, 16, 4):
        print(f"s[{i:2}]: 0x{state[i]:08x}  s[{i+1:2}]: 0x{state[i+1]:08x}  s[{i+2:2}]: 0x{state[i+2]:08x}  s[{i+3:2}]: 0x{state[i+3]:08x}")
    print()

#1. Initialzustand aus Aufgabe 2.2 definieren
initial_state_1 = [
    0x11111111, 0x01020304, 0x9b8d6f43, 0x01234567,
    0x22222222, 0x01020304, 0x9b8d6f43, 0x01234567,
    0x33333333, 0x01020304, 0x9b8d6f43, 0x01234567,
    0x44444444, 0x01020304, 0x9b8d6f43, 0x01234567
]

#Kopieren, damit wir den Originalzustand nicht überschreiben
state_1 = initial_state_1.copy()

#2. Erste Double Round durchführen
double_round(state_1)
print_state(state_1, "Zustand nach 1. Double Round")

#3. Zweiten Zustand initialisieren
initial_state_2 = initial_state_1.copy()
initial_state_2[0] = 0x11111110  #Änderung

state_2 = initial_state_2.copy()

#4. Zweite Double Round durchführen
double_round(state_2)
print_state(state_2, "Zustand nach 2. Double Round (mit modifiziertem s[0])")

#5. XOR-Differenz berechnen und anzeigen
diff_state = []
for i in range(16):
    diff = state_1[i] ^ state_2[i]
    diff_state.append(diff)

print_state(diff_state, "XOR-Differenz beider Berechnungen")

bit_flips = sum(bin(diff).count('1') for diff in diff_state)
print(f"Anzahl der veränderten Bits nach nur einer Double Round: {bit_flips} von 512 Bits.")