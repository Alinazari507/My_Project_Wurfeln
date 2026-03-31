import os
import json
import yaml
import xml.etree.ElementTree as ET
from datetime import datetime
import random

# --- Dateimanagement (Lektion P2_2_5 Fokus) ---

def generiere_dateiname(extension):
    """
    Erzeugt einen Dateinamen mit aktuellem Datum und Uhrzeit.
    Beispiel: save_20260217_1115.json
    """
    zeitstempel = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"save_{zeitstempel}.{extension}"

def finde_speicherstaende():
    """
    Scannt das Verzeichnis nach Dateien, die mit 'save_' beginnen.
    """
    alle_dateien = os.listdir(".")
    valid_extensions = (".json", ".yaml", ".xml")
    # Filtern der Dateien nach Präfix und Endung
    saves = [f for f in alle_dateien if f.startswith("save_") and f.endswith(valid_extensions)]
    return sorted(saves, reverse=True)

# --- Speichern und Laden ---

def statistik_speichern(statistik, format_wahl):
    """
    Speichert die Statistik in einer neuen Datei mit Zeitstempel.
    """
    if format_wahl == "x":
        ext = "xml"
    elif format_wahl == "y":
        ext = "yaml"
    else:
        ext = "json"

    dateiname = generiere_dateiname(ext)

    if ext == "xml":
        root = ET.Element("Statistik")
        for index, value in enumerate(statistik, start=1):
            wurf = ET.SubElement(root, "Wurf")
            wurf.set("seite", str(index))
            wurf.text = str(value)
        tree = ET.ElementTree(root)
        tree.write(dateiname, encoding="utf-8", xml_declaration=True)
    elif ext == "yaml":
        with open(dateiname, "w") as f:
            yaml.safe_dump(statistik, f)
    else:
        with open(dateiname, "w") as f:
            json.dump(statistik, f, indent=4)

    print(f"✅ Spielstand gespeichert: {dateiname}")

def statistik_laden(dateiname):
    """
    Lädt Daten aus einer spezifischen Datei und validiert die Struktur.
    """
    try:
        if dateiname.endswith(".xml"):
            tree = ET.parse(dateiname)
            root = tree.getroot()
            daten = []
            for wurf in root.findall("Wurf"):
                wert = wurf.text if wurf.text is not None else "0"
                daten.append(int(wert))
            return daten if len(daten) == 6 else [0]*6
        elif dateiname.endswith(".yaml"):
            with open(dateiname, "r") as f:
                return yaml.safe_load(f)
        else:
            with open(dateiname, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"❌ Fehler beim Laden: {e}")
        return [0, 0, 0, 0, 0, 0]

# --- Hauptprogramm ---

def main():
    saves = finde_speicherstaende()
    ergebnisse = [0, 0, 0, 0, 0, 0]

    print("🎲 WÜRFELSPIEL - VERSION P2.2.5")

    # Auswahl-Menü für vorhandene Spielstände
    if saves:
        print("\n--- Gefundene Spielstände ---")
        for i, datei in enumerate(saves, start=1):
            print(f"{i}. {datei}")
        print("0. Neues Spiel starten")

        wahl = input("\nWelche Nummer laden? (0 für neu): ")
        if wahl.isdigit() and 0 < int(wahl) <= len(saves):
            dateiname = saves[int(wahl)-1]
            ergebnisse = statistik_laden(dateiname)
            print(f"📂 {dateiname} geladen.")

    while True:
        print(f"\nAktuelle Statistik: {ergebnisse}")
        befehl = input("Enter (Würfeln) | 's' (Speichern & Beenden): ").lower().strip()

        if befehl == "":
            wurf = random.randint(1, 6)
            ergebnisse[wurf-1] += 1
            print(f"🎲 Ergebnis: {wurf}")
        elif befehl == "s":
            fmt = input("Format: [j]son, [y]aml, [x]ml: ").lower().strip()
            statistik_speichern(ergebnisse, fmt)
            break

if __name__ == "__main__":
    main()