import random

# Konstanten
AUGEN_MIN = 1
AUGEN_MAX = 6

def wuerfeln():
    # Nutzt die Konstanten statt fixer Zahlen
    return random.randint(AUGEN_MIN, AUGEN_MAX)

ergebnisse_liste = []

while True:
    ergebnis = wuerfeln()
    ergebnisse_liste.append(ergebnis)

    print(f"Wurf Nr. {len(ergebnisse_liste)}: {ergebnis}")

    entscheidung = input("Nochmal würfeln? (ja/nein): ")

    if entscheidung.lower() == "nein":
        print("\n--- Statistik ---")
        # Hier nutzen wir AUGEN_MAX + 1 für die Range-Logik
        for zahl in range(AUGEN_MIN, AUGEN_MAX + 1):
            anzahl = ergebnisse_liste.count(zahl)
            print(f"Zahl {zahl}: {anzahl} Mal")

        print(f"Gesamtanzahl: {len(ergebnisse_liste)}")
        break