import random

# Konstanten
AUGEN_MIN = 1
AUGEN_MAX = 6

def wuerfeln() -> int:
    """Simuliert einen Würfelwurf."""
    return random.randint(AUGEN_MIN, AUGEN_MAX)

def main() -> None:
    # Initialisierung der flüchtigen Daten (Statelessness)
    ergebnisse_liste = []

    print("--- Würfelspiel gestartet ---")

    while True:
        # Würfelvorgang
        ergebnis = wuerfeln()
        ergebnisse_liste.append(ergebnis)

        print(f"Wurf Nr. {len(ergebnisse_liste)}: {ergebnis}")

        # Benutzereingabe für erneuten Wurf
        entscheidung = input("Nochmal würfeln? (ja/nein): ")

        if entscheidung.lower() == "nein":
            # Analyse der Ergebnisse (Gleichverteilung prüfen)
            print("\n--- Statistik dieser Spielrunde ---")
            for zahl in range(AUGEN_MIN, AUGEN_MAX + 1):
                anzahl = ergebnisse_liste.count(zahl)
                print(f"Zahl {zahl}: {anzahl} Mal")

            print(f"Gesamtanzahl der Würfe: {len(ergebnisse_liste)}")

            # Realisierung der Statelessness: Daten werden nicht gespeichert
            ergebnisse_liste.clear()
            print("\n[INFO] Alle Daten wurden aus dem Arbeitsspeicher gelöscht.")
            print("[INFO] Keine Speicherung erfolgt. Programm beendet.")
            break

if __name__ == "__main__":
    main()