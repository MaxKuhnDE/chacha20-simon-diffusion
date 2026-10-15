print("Aufgabe 2.5 - Simon 128/128 (Mit Key-Scheduler und variablen Runden)")

def rotl64(x, c):
    """Führt eine bitweise Linksrotation für 64-Bit Integer durch."""
    return ((x << c) & 0xFFFFFFFFFFFFFFFF) | (x >> (64 - c))

def simon_round(s, k_round):
    """Führt EINE Runde Simon aus."""
    x = s[0]  # Linke Hälfte (L)
    y = s[1]  # Rechte Hälfte (R)
    
    # f(x) = ((x <<< 1) & (x <<< 8)) ^ (x <<< 2)
    tmp1 = rotl64(x, 1)
    tmp2 = rotl64(x, 8)
    tmp3 = rotl64(x, 2)
    f_x = (tmp1 & tmp2) ^ tmp3
    
    # Kreuztausch (Feistel)
    new_x = y ^ f_x ^ k_round  # Neues s[0] (Links)
    new_y = x                  # Neues s[1] (Rechts)
    
    return [new_x, new_y]

def generate_key_schedule(k, num_rounds):
    """
    Generiert alle benötigten Rundenschlüssel für Simon 128/128 (m=2).
    k ist eine Liste mit den Startschlüsseln [k_0, k_1].
    """
    keys = k.copy()
    c = 0xfffffffffffffffc
    # Die korrekte z2-Sequenz für Simon 128/128 (Periode 62)
    z2 = [1,0,1,0,1,1,1,1,0,1,1,1,0,0,0,0,0,0,1,1,0,1,0,0,1,0,0,1,1,0,0,0,
          1,0,1,0,0,0,0,1,0,0,0,1,1,1,1,1,1,0,0,1,0,1,1,0,1,1,0,0,1,1]
    
    # Wir berechnen so viele Schlüssel, wie wir Runden haben
    for i in range(num_rounds - 2): # -2, da wir k[0] und k[1] schon haben
        tmp = rotl64(keys[i+1], 61)             # entspricht (k[i+1] >>> 3)
        tmp = tmp ^ rotl64(tmp, 63)             # entspricht tmp ^ (tmp >>> 1)
        
        # k[i+2] = k[i] ^ tmp ^ c ^ z_2[i mod 62]
        new_k = keys[i] ^ tmp ^ c ^ z2[i % 62]
        keys.append(new_k)
        
    return keys

def print_state(state, title="State"):
    print(f"--- {title} ---")
    print(f"s[0] (Links) : 0x{state[0]:016x}")
    print(f"s[1] (Rechts): 0x{state[1]:016x}\n")

# --- Benutzereingabe ---
try:
    num_rounds = int(input("Wie viele Simon-Runden sollen berechnet werden? (z.B. 1 bis 68): "))
    if num_rounds < 1: num_rounds = 1
except ValueError:
    print("Ungültige Eingabe. Setze auf 1 Runde.")
    num_rounds = 1

# --- Setup Parameter ---
initial_s = [0x1111111111111111, 0x0102030405060708]
initial_k = [0xFFEEDDCCBBAA9988, 0x7766554433221100]

# Generiere den Key-Schedule für die gewünschte Anzahl Runden
# (Wir erzwingen mind. 2 Schlüssel, falls jemand nur 1 Runde eingibt)
round_keys = generate_key_schedule(initial_k, max(num_rounds, 2))

# --- Originalzustand berechnen ---
state_1 = initial_s.copy()
for i in range(num_rounds):
    state_1 = simon_round(state_1, round_keys[i])
print_state(state_1, f"Zustand nach {num_rounds} Runde(n) (Original)")

# --- Modifizierten Zustand berechnen (1 Bit Flip in s[0]) ---
initial_s2 = initial_s.copy()
initial_s2[0] = 0x1111111111111110 
state_2 = initial_s2.copy()
for i in range(num_rounds):
    state_2 = simon_round(state_2, round_keys[i])
print_state(state_2, f"Zustand nach {num_rounds} Runde(n) (mit Bit Flip)")

# --- Auswertung: XOR-Differenz ---
diff_state = [
    state_1[0] ^ state_2[0],
    state_1[1] ^ state_2[1]
]

print_state(diff_state, "XOR-Differenz beider Berechnungen")

bit_flips = sum(bin(diff).count('1') for diff in diff_state)
prozent = (bit_flips / 128) * 100
print(f"Ergebnis: Nach {num_rounds} Runde(n) haben sich {bit_flips} von 128 Bits geändert ({prozent:.2f}%).")