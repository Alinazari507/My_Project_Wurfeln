import json
import os
import random

# Konstante für den Dateinamen definieren
FILENAME = "dice_results.json"

# --- SCHRITT 1: Laden des Spielstands (Deserialisierung) ---

# Prüfen, ob die Datei existiert, um Laufzeitfehler zu vermeiden
if os.path.exists(FILENAME):
    # Datei im Lesemodus ("r") öffnen
    with open(FILENAME, "r") as file:
        # JSON-Daten in ein Python-Dictionary umwandeln
        data = json.load(file)
        # Die Historie aus dem Dictionary extrahieren
        ergebnisse_liste = data["history"]

    print(f"✅ Spielstand geladen! Bisherige Würfe: {len(ergebnisse_liste)}")
else:
    # Falls keine Datei existiert, mit einer leeren Liste starten
    ergebnisse_liste = []
    print("ℹ️ Kein alter Spielstand gefunden. Ein neues Spiel beginnt.")

# --- SCHRITT 2: Spiel-Loop und Speichern (Serialisierung) ---

print("\n--- Würfelspiel-Fortsetzung ---")

while True:
    aktion = input("Drücke 'w' zum Würfeln oder 'q' zum Beenden: ").lower().strip()

    if aktion == "w":
        # Würfeln und zur Liste hinzufügen
        wurf = random.randint(1, 6)
        ergebnisse_liste.append(wurf)
        print(f"🎲 Würfelergebnis: {wurf} (Gesamt: {len(ergebnisse_liste)})")

        # Daten für die Speicherung vorbereiten
        data_to_save = {
            "total": len(ergebnisse_liste),
            "history": ergebnisse_liste
        }

        # Sofortiges Speichern nach jedem Wurf (Datensicherheit)
        with open(FILENAME, "w") as file:
            json.dump(data_to_save, file, indent=4)

    elif aktion == "q":
        print("👋 Spiel beendet. Dein Fortschritt ist sicher gespeichert!")
        break
    else:
        print("⚠️ Ungültige Eingabe! Bitte 'w' oder 'q' nutzen.")