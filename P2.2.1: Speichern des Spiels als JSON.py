import random
import json

# Dateiname für die Speicherung definieren
FILENAME = "dice_results.json"

# Eine leere Liste erstellen, um die Historie der Ergebnisse zu speichern
ergebnisse_liste = []

print("🎲 Willkommen zum Würfelspiel (Lektion P2.2.1)")

while True:
    # Benutzereingabe abfragen und Leerzeichen entfernen
    decision = input("Möchten Sie würfeln? (ja/nein): ").lower().strip()

    if decision == "ja":
        # Würfeln und das Ergebnis der Liste hinzufügen
        ergebnis = random.randint(1, 6)
        ergebnisse_liste.append(ergebnis)

        # Aktuellen Wurf in der Konsole anzeigen
        print(f"Wurf Nr. {len(ergebnisse_liste)}: {ergebnis}")

    elif decision == "nein":
        # Die Statistik für die JSON-Datei vorbereiten (Strukturierung als Dictionary)
        stats = {
            "total": len(ergebnisse_liste), # Anzahl der Würfe
            "history": ergebnisse_liste     # Liste der Ergebnisse
        }

        # Daten in der JSON-Datei speichern (Serialisierung)
        # indent=4 sorgt für eine menschenlesbare Struktur
        with open(FILENAME, "w") as file:
            json.dump(stats, file, indent=4)

        print(f"✅ Spiel beendet und Daten erfolgreich in '{FILENAME}' gespeichert!")
        break

    else:
        # Fehlermeldung bei ungültiger Eingabe
        print("⚠️ Bitte geben Sie nur 'ja' oder 'nein' ein.")
