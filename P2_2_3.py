import os
import random
import json
import yaml # Externe Bibliothek: Installation via 'pip install pyyaml'

# Definition der Dateinamen
DATEI_JSON = "spiel_statistik.json"
DATEI_YAML = "spiel_statistik.yaml"

def statistik_speichern(statistik, format_wahl):
    """
    Speichert die Statistik basierend auf der Wahl (j/y) im entsprechenden Format.
    """
    if format_wahl == "y":
        # Speichern im YAML-Format
        with open(DATEI_YAML, "w") as f:
            yaml.safe_dump(statistik, f)
        print(f"✅ Statistik erfolgreich in {DATEI_YAML} gespeichert.")
    else:
        # Standard: Speichern im JSON-Format
        with open(DATEI_JSON, "w") as f:
            json.dump(statistik, f, indent=4)
        print(f"✅ Statistik erfolgreich in {DATEI_JSON} gespeichert.")

def statistik_laden():
    """
    Prüft die Existenz von Dateien und lädt den Spielstand.
    Priorität: YAML > JSON > Neu (Default).
    """
    if os.path.exists(DATEI_YAML):
        with open(DATEI_YAML, "r") as f:
            print("📂 Lade vorhandenen Spielstand aus YAML...")
            return yaml.safe_load(f)
    elif os.path.exists(DATEI_JSON):
        with open(DATEI_JSON, "r") as f:
            print("📂 Lade vorhandenen Spielstand aus JSON...")
            return json.load(f)

    # Rückgabe einer leeren Statistik (6 Seiten des Würfels)
    return [0, 0, 0, 0, 0, 0]

def main():
    # Initialisierung: Spielstand laden
    statistik = statistik_laden()

    print("🎲 WÜRFELSPIEL - VERSION P2.2.3")
    print("------------------------------")

    while True:
        eingabe = input("\n[Enter] Würfeln | [s] Statistik | [q] Beenden & Speichern: ").lower().strip()

        if eingabe == "":
            # Logik für das Würfeln
            wurf = random.randint(1, 6)
            statistik[wurf-1] += 1
            print(f"Ergebnis: {wurf} (Wurf Nr. {sum(statistik)})")

        elif eingabe == "s":
            # Aktuelle Statistik anzeigen
            print("\n--- AKTUELLE STATISTIK ---")
            for i, wert in enumerate(statistik, 1):
                print(f"Zahl {i}: {wert}x")
            print(f"Gesamtanzahl: {sum(statistik)}")

        elif eingabe == "q":
            # Abfrage des Speicherformats ohne فارسی (nur Deutsch)
            wahl = input("Welches Format? ([j] für JSON / [y] für YAML): ").lower().strip()
            statistik_speichern(statistik, wahl)
            print("Programm wird beendet. Auf Wiedersehen!")
            break
        else:
            print("❌ Ungültige Eingabe. Bitte versuchen Sie es erneut.")

if __name__ == "__main__":
    main()
