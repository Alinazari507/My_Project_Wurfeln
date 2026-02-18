import os
import random
import json
import yaml
import xml.etree.ElementTree as ET

# Konfiguration der Dateinamen
DATEI_JSON = "spiel_statistik.json"
DATEI_YAML = "spiel_statistik.yaml"
DATEI_XML = "spiel_statistik.xml"

def statistik_speichern(statistik, format_wahl):
    """
    Speichert die aktuelle Statistik in das gewählte Format (JSON, YAML oder XML).
    """
    if format_wahl == "x":
        # Erstellung der XML
        root = ET.Element("Statistik")
        for index, value in enumerate(statistik, start=1):
            wurf_element = ET.SubElement(root, "Wurf")
            wurf_element.set("seite", str(index))
            wurf_element.text = str(value)

        # Speichern der XML-Datei
        tree = ET.ElementTree(root)
        tree.write(DATEI_XML, encoding="utf-8", xml_declaration=True)
        print(f"✅ Erfolg: gespeichert in {DATEI_XML}")

    elif format_wahl == "y":
        with open(DATEI_YAML, "w") as f:
            yaml.safe_dump(statistik, f)
        print(f"✅ Erfolg: gespeichert in {DATEI_YAML}")

    else:
        with open(DATEI_JSON, "w") as f:
            json.dump(statistik, f, indent=4)
        print(f"✅ Erfolg: gespeichert in {DATEI_JSON}")

def statistik_laden():
    """
    Lädt die Statistik aus einer Datei. Priorität: XML > YAML > JSON.
    Verhindert IndexError durch Validierung der Listenlänge.
    """
    daten = [0, 0, 0, 0, 0, 0] # Standardwerte (Fallback)

    # XML laden
    if os.path.exists(DATEI_XML):
        try:
            print("📂 Lade Spielstand aus XML...")
            tree = ET.parse(DATEI_XML)
            root = tree.getroot()
            temp_daten = []
            for wurf in root.findall("Wurf"):
                # Sicherer Umgang mit Text-Werten
                text_wert = wurf.text if wurf.text is not None else "0"
                temp_daten.append(int(text_wert))

            # Validierung: Nur zurückgeben, wenn 6 Seiten vorhanden sind
            if len(temp_daten) == 6:
                return temp_daten
        except Exception as e:
            print(f"⚠️ XML Fehler: {e}. Nutze Standardwerte.")

    # YAML laden
    elif os.path.exists(DATEI_YAML):
        with open(DATEI_YAML, "r") as f:
            temp_yaml = yaml.safe_load(f)
            if isinstance(temp_yaml, list) and len(temp_yaml) == 6:
                return temp_yaml

    # JSON laden
    elif os.path.exists(DATEI_JSON):
        with open(DATEI_JSON, "r") as f:
            temp_json = json.load(f)
            if isinstance(temp_json, list) and len(temp_json) == 6:
                return temp_json

    return daten

def main():
    # Initialer Zustand laden
    statistik = statistik_laden()

    print("🎲 WÜRFELSPIEL - LEKTION P2.2.4 (XML SUPPORT)")

    while True:
        # Sicherstellen, dass statistik eine Liste ist und nicht leer (Bug-Prävention)
        if not statistik or len(statistik) != 6:
            statistik = [0, 0, 0, 0, 0, 0]

        print(f"\nAktueller Stand: {statistik}")
        eingabe = input("[Enter] Würfeln | [s] Speichern & Beenden: ").lower().strip()

        if eingabe == "":
            wurf = random.randint(1, 6)
            # Zugriff auf Index (0 bis 5)
            statistik[wurf-1] += 1
            print(f"🎲 Ergebnis: {wurf}")
        elif eingabe == "s":
            wahl = input("Format wählen (j/y/x): ").lower().strip()
            statistik_speichern(statistik, wahl)
            break
        else:
            print("❌ Ungültige Eingabe.")

if __name__ == "__main__":
    main()