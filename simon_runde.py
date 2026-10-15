print("Aufgabe 2.4 - Simon 128/128")

def rotl64(x, c):
    """Führt eine bitweise Linksrotation für 64-Bit Integer durch."""
    return ((x << c) & 0xFFFFFFFFFFFFFFFF) | (x >> (64 - c))

def simon_round(s, k_round):
    """
    s[1] = Linke Hälfte (L)
    s[0] = Rechte Hälfte (R)
    """
    x = s[0]  # Linke Hälfte
    y = s[1]  # Rechte Hälfte
    
    # f(x) = ((x <<< 1) & (x <<< 8)) ^ (x <<< 2)
    tmp1 = rotl64(x, 1)
    tmp2 = rotl64(x, 8)
    tmp3 = rotl64(x, 2)
    f_x = (tmp1 & tmp2) ^ tmp3
    
    # Neue linke Hälfte = R ^ f(L) ^ K
    # Neue rechte Hälfte = L
    new_x = y ^ f_x ^ k_round  # Dies wird das neue s[1] (Links)
    new_y = x                  # Dies wird das neue s[0] (Rechts)
    
    # Rückgabe im Format [Rechtes Wort, Linkes Wort]
    return [new_y, new_x]

def print_state(state, title="State"):
    print(f"--- {title} ---")
    print(f"s[0] (Rechts): 0x{state[0]:016x}")
    print(f"s[1] (Links) : 0x{state[1]:016x}\n")

initial_s = [0x1111111111111111, 0x0102030405060708]
k = [0xFFEEDDCCBBAA9988, 0x7766554433221100]

state_1 = initial_s.copy()
state_1 = simon_round(state_1, k[0])
print_state(state_1, "Zustand nach 1. Runde (Original)")

initial_s2 = initial_s.copy()
initial_s2[0] = 0x1111111111111110 

state_2 = initial_s2.copy()
state_2 = simon_round(state_2, k[0])
print_state(state_2, "Zustand nach 1. Runde (mit modifiziertem s[0])")

#XOR-Differenz berechnen und anzeigen
diff_state = [
    state_1[0] ^ state_2[0],
    state_1[1] ^ state_2[1]
]

print_state(diff_state, "XOR-Differenz beider Berechnungen")

bit_flips = sum(bin(diff).count('1') for diff in diff_state)
print(f"Anzahl der veränderten Bits nach 1 Simon-Runde: {bit_flips} von 128 Bits.")