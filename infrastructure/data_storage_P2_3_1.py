import json
import os

def save_players(player_list):
    """
    Speichert die Liste der Spielernamen dauerhaft in einer JSON-Datei.
    Erstellt den Ordner automatisch, falls er nicht existiert.
    """
    directory = "resources"
    filename = f"{directory}/players.json"
    
    try:
        # Sicherstellen, dass das Verzeichnis existiert
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        # Speichern mit UTF-8, um deutsche Umlaute (ä, ö, ü) zu unterstützen
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(player_list, f, indent=4, ensure_ascii=False)
            
        print(f"✅ Spielerliste erfolgreich in {filename} gespeichert.")
    except Exception as e:
        print(f"❌ Fehler beim Speichern der Daten: {e}")

def load_players():
    """
    Lädt die Spielerliste aus der JSON-Datei.
    Gibt eine leere Liste zurück, falls die Datei nicht existiert oder leer ist.
    """
    filename = "resources/players.json"
    
    if not os.path.exists(filename):
        return []
        
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Falls die Datei korrupt oder leer ist, eine leere Liste zurückgeben
        return []