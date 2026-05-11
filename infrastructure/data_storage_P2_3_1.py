import json
import os

"""
INFRASTRUCTURE LAYER: Data Storage
Dieses Modul ist für das Speichern und Laden von Daten zuständig.
Es enthält keine Prints, um die Trennung der Schichten (Separation of Concerns) zu wahren.
"""

def save_players(player_list):
    """
    Speichert die Liste der Spielernamen dauerhaft in einer JSON-Datei.
    """
    directory = "resources"
    filename = f"{directory}/players.json"
    
    try:
        # Sicherstellen, dass das Verzeichnis existiert
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        # Speichern mit UTF-8 Unterstützung
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(player_list, f, indent=4, ensure_ascii=False)
            
        # Wir geben True zurück, damit die Application-Layer weiß, dass es geklappt hat
        return True
    except Exception as e:
        # Wir reichen den Fehler weiter an die Application-Layer
        raise IOError(f"Fehler beim Speichern in {filename}: {str(e)}")

def load_players():
    """
    Lädt die Spielerliste aus der JSON-Datei.
    """
    filename = "resources/players.json"
    
    if not os.path.exists(filename):
        return []
        
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    