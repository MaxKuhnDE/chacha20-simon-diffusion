# ChaCha20 und Simon: Diffusion

Python-Implementierungen der ChaCha20-Quarterround und -Doubleround (nach RFC 7539) sowie der Blockchiffre Simon128/128 mit Key-Schedule. Damit wird untersucht, wie sich ein einzelnes gekipptes Eingabebit über die Runden ausbreitet (Lawineneffekt). Entstanden im Praktikum 2 im Fach Kryptografie (Sommersemester 2026, Hochschule Albstadt-Sigmaringen).

Rotationen und Bitoperationen sind selbst geschrieben, es wird keine externe Bibliothek verwendet.

## Dateien

| Datei | Aufgabe | Inhalt |
|---|---|---|
| `chacha20_doubleround.py` | 2.2 | eine ChaCha20-Doubleround und XOR-Differenz bei gekipptem Bit in s[0] |
| `chacha20_avalanche.py` | 2.3 | wie 2.2, Anzahl der Doublerounds wird abgefragt |
| `simon_runde.py` | 2.4 | eine Runde Simon128/128 und XOR-Differenz |
| `simon_avalanche.py` | 2.5 | Simon128/128 mit Key-Schedule, Rundenzahl wird abgefragt (1 bis 68) |

## Aufruf

```bash
python3 chacha20_doubleround.py
python3 chacha20_avalanche.py     # fragt nach der Anzahl Doublerounds
python3 simon_runde.py
python3 simon_avalanche.py        # fragt nach der Anzahl Runden
```

Alle Skripte vergleichen zwei Berechnungen: einmal mit dem Ausgangszustand, einmal mit `s[0]`, bei dem das niedrigste Bit gekippt ist (`…1111` → `…1110`). Ausgegeben werden beide Zustände, die XOR-Differenz und die Anzahl der veränderten Bits.

## ChaCha20

### Aufgabe 2.1: Quarterround von Hand

```
a += b; d ^= a; d <<<= 16;
c += d; b ^= c; b <<<= 12;
a += b; d ^= a; d <<<= 8;
c += d; b ^= c; b <<<= 7;
```

Mit a = `0x11111111`, b = `0x01020304`, c = `0x9b8d6f43`, d = `0x01234567` ergibt sich

```
a = 0xea2a92f4   b = 0xcb1cf8ce   c = 0x4581472e   d = 0x5881c4bb
```

Das entspricht dem Testvektor in RFC 7539, Abschnitt 2.1.1. Die Funktion `quarter_round()` in den Skripten liefert dasselbe Ergebnis.

### Aufgabe 2.2: Doubleround

Der Zustand aus 16 Wörtern wird als 4×4-Matrix in Zeilenreihenfolge gelesen. Eine Doubleround besteht aus

- einer **Column-Round**: Quarterround auf die vier Spalten (0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15)
- einer **Diagonal-Round**: Quarterround auf die vier Diagonalen (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14)

ChaCha20 besteht aus 10 solchen Doublerounds, also 20 Runden.

XOR-Differenz nach einer Doubleround, wenn nur das niedrigste Bit von s[0] gekippt wird:

```
s[ 0]: 0x21000001  s[ 1]: 0x00100033  s[ 2]: 0x101d0030  s[ 3]: 0x133d6b99
s[ 4]: 0xb349af83  s[ 5]: 0x3868f18f  s[ 6]: 0x61f61821  s[ 7]: 0x0a09a812
s[ 8]: 0x34011340  s[ 9]: 0x761ae1d1  s[10]: 0x0d70d1e3  s[11]: 0x42d3ec03
s[12]: 0x40013301  s[13]: 0x1d003010  s[14]: 0x1aea21fb  s[15]: 0x03300121
```

Schon nach einer Doubleround hat sich jedes der 16 Wörter verändert, insgesamt 178 von 512 Bits.

### Aufgabe 2.3: mehrere Doublerounds

| Doublerounds | veränderte Bits | Anteil |
|---|---|---|
| 1 | 178 von 512 | 34,77 % |
| 2 | 246 von 512 | 48,05 % |
| 3 | 240 von 512 | 46,88 % |
| 4 | 265 von 512 | 51,76 % |

Beobachtung: Es setzt ein Lawineneffekt ein. Ab zwei Doublerounds ist etwa die Hälfte aller Bits verändert, das ist der Wert, den man bei zufälligen Daten erwartet. Zwischen 2, 3 und 4 Doublerounds gibt es keinen großen Unterschied mehr, der Wert schwankt nur noch um 50 %.

## Simon128/128

### Aufgabe 2.4: eine Runde

Simon ist eine Feistel-Chiffre mit zwei 64-Bit-Wörtern (links x, rechts y). Eine Runde mit Rundenschlüssel k:

```
f(x)  = ((x <<< 1) & (x <<< 8)) ^ (x <<< 2)
x_neu = y ^ f(x) ^ k
y_neu = x
```

Im Eingabezustand ist `s[0]` das linke Wort, das in f eingeht. `simon_runde.py` gibt das Ergebnis in der Reihenfolge s[0] = rechtes, s[1] = linkes Wort aus; `simon_avalanche.py` behält s[0] = links, s[1] = rechts bei, wie es für die nächste Runde gebraucht wird. Startwerte: s[0] = `0x1111111111111111`, s[1] = `0x0102030405060708`, k[0] = `0xFFEEDDCCBBAA9988`, k[1] = `0x7766554433221100`.

Ergebnis nach einer Runde (Ausgabe von `simon_runde.py`):

```
--- XOR-Differenz beider Berechnungen ---
s[0] (Rechts): 0x0000000000000001
s[1] (Links) : 0x0000000000000004

Anzahl der veränderten Bits nach 1 Simon-Runde: 2 von 128 Bits.
```

Das gekippte Bit wandert unverändert ins neue rechte Wort. Im neuen linken Wort ändert sich nur Bit 2, weil es über `x <<< 2` hineinkommt. Die beiden UND-Terme ändern sich nicht, da die Partnerbits an diesen Stellen 0 sind.

### Aufgabe 2.5: 2 bis 10 Runden mit Key-Schedule

Für Simon128/128 (m = 2 Schlüsselwörter) werden die weiteren Rundenschlüssel so berechnet:

```
tmp    = k[i+1] >>> 3
tmp    = tmp ^ (tmp >>> 1)
k[i+2] = k[i] ^ tmp ^ c ^ z2[i mod 62]      mit c = 0xfffffffffffffffc
```

| Runden | veränderte Bits | Anteil |
|---|---|---|
| 1 | 2 von 128 | 1,56 % |
| 2 | 5 von 128 | 3,91 % |
| 3 | 7 von 128 | 5,47 % |
| 4 | 11 von 128 | 8,59 % |
| 5 | 19 von 128 | 14,84 % |
| 6 | 23 von 128 | 17,97 % |
| 7 | 28 von 128 | 21,88 % |
| 8 | 33 von 128 | 25,78 % |
| 9 | 39 von 128 | 30,47 % |
| 10 | 51 von 128 | 39,84 % |

Beobachtung: Je mehr Runden, desto mehr Bits ändern sich. Im Vergleich zu ChaCha20 wächst die Zahl aber viel langsamer: Nach 10 Runden sind erst etwa 40 % der Bits verändert, während ChaCha20 schon nach zwei Doublerounds bei rund 50 % liegt. Das liegt daran, dass bei Simon pro Runde nur eine Hälfte des Zustands neu berechnet wird und die einzige nichtlineare Operation das UND in f ist. Simon128/128 verwendet insgesamt 68 Runden.

### Prüfung mit dem offiziellen Testvektor

`simon_avalanche.py` wurde mit dem Testvektor für Simon128/128 aus dem Simon-und-Speck-Paper (Beaulieu et al., 2013, https://eprint.iacr.org/2013/404) geprüft. Mit 68 Runden, Schlüssel `0f0e0d0c0b0a0908 0706050403020100` und Klartext `6373656420737265 6c6c657661727420` ergibt sich wie erwartet das Chiffrat `49681b1e1e54fe3f 65aa832af84e0bbc`.

## Entstehung

Der Code ist im Rahmen des Praktikums entstanden. Diese Dokumentation wurde mit Hilfe von Claude (Anthropic) auf Basis der Abgabe erstellt.
