import json
import os
from datetime import datetime

def save_game_result(game):
    """ Speichert den Endstand des Spiels in einer JSON-Datei. """
    directory = "resources/history"
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{directory}/result_{timestamp}.json"
    
    data = {
        "date": timestamp,
        "final_scores": game.get_final_scores(),
        "total_rounds": game.max_rounds
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\n💾 Spielstand wurde unter {filename} gespeichert.")