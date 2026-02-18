import random
from typing import List # Für die strikte Typisierung

# --- Konstanten ---
AUGEN_MIN: int = 1
AUGEN_MAX: int = 6

# --- Logik (Klasse) ---
class Wuerfel:
    """
    Diese Klasse kapselt die Logik des Würfels (Trennung von Geschäftslogik und E/A).
    """
    def __init__(self, min_augen: int = AUGEN_MIN, max_augen: int = AUGEN_MAX):
        self.min: int = min_augen
        self.max: int = max_augen

    def wuerfeln(self) -> int:
        """Führt einen Würfelwurf aus und gibt das Ergebnis zurück."""
        return random.randint(self.min, self.max)

# --- Funktionen für die Statistik ---
def erstelle_statistik(ergebnisse: List[int]) -> None:
    """Erstellt die Statistik-Ausgabe (Trennung der Ausgabe-Logik)."""
    print("\n--- Statistik ---")
    for zahl in range(AUGEN_MIN, AUGEN_MAX + 1):
        anzahl = ergebnisse.count(zahl)
        print(f"Zahl {zahl}: {anzahl} Mal")
    print(f"Gesamtanzahl: {len(ergebnisse)}")

# --- Hauptprogramm (Eingabe/Ausgabe) ---
def main() -> None:
    mein_wuerfel = Wuerfel() # Instanz der Klasse erstellen
    ergebnisse_liste: List[int] = []

    while True:
        ergebnis: int = mein_wuerfel.wuerfeln()
        ergebnisse_liste.append(ergebnis)

        print(f"Wurf Nr. {len(ergebnisse_liste)}: {ergebnis}")

        entscheidung: str = input("Nochmal würfeln? (ja/nein): ").strip().lower()

        if entscheidung == "nein":
            erstelle_statistik(ergebnisse_liste)
            break

if __name__ == "__main__":
    main()