import json
import os
import random

FILENAME = "dice_results.json"

# --- 1. LADEN (Deserialisierung) ---
if os.path.exists(FILENAME):
    with open(FILENAME, "r") as file:
        data = json.load(file)
        ergebnisse_liste = data["history"]
    print(f"✅ Spielstand geladen! Bisherige Würfe: {len(ergebnisse_liste)}")
else:
    ergebnisse_liste = []
    print("ℹ️ Kein Spielstand gefunden. Ein neues Spiel beginnt.")

# --- 2. SPIEL-LOOP & SPEICHERN ---
while True:
    aktion = input("Drücke 'w' zum Würfeln oder 'q' zum Beenden: ").lower()

    if aktion == "w":
        wurf = random.randint(1, 6)
        ergebnisse_liste.append(wurf)
        print(f"🎲 Würfelergebnis: {wurf}")

        # Sofortiges Speichern nach jedem Wurf
        data_to_save = {
            "total": len(ergebnisse_liste),
            "history": ergebnisse_liste
        }
        with open(FILENAME, "w") as file:
            json.dump(data_to_save, file, indent=4)
        print("💾 Fortschritt gespeichert.")

    elif aktion == "q":
        print("Programm beendet. 👋")
        break