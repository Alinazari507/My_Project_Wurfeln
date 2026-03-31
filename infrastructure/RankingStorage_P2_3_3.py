"""
P2.3.3: Rangliste nach jeder Runde - INFRASTRUCTURE LAYER

Verantwortung: Persistierung und Ranglisten-Speicherung
- Speichern von Ranglisten
- Laden von Ranglisten-Historie
- Ranglisten-Statistiken
"""

import json
import os
from datetime import datetime
from domain.Ranking_P2_3_3 import Ranking


def save_ranking_snapshot(game, round_number):
    """
    Speichert eine Ranglisten-Momentaufnahme nach einer Runde.
    
    Args:
        game (GameRound): Das aktuelle Spiel
        round_number (int): Rundenummer
        
    Returns:
        str: Pfad zur gespeicherten Datei oder None
    """
    directory = "resources"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{directory}/ranking_round{round_number}_{timestamp}.json"
    
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Erstelle Rangliste
        ranking = Ranking(game.player_scores)
        ranking_list = ranking.get_ranking_with_rank()
        
        # Daten vorbereiten
        ranking_data = {
            "timestamp": datetime.now().isoformat(),
            "round": round_number,
            "ranking": [
                {
                    "rank": rank,
                    "player": player,
                    "score": score
                }
                for rank, player, score in ranking_list
            ]
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(ranking_data, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Rangliste Runde {round_number} in {filename} gespeichert.")
        return filename
    except Exception as e:
        print(f"❌ Fehler beim Speichern der Rangliste: {e}")
        return None


def load_ranking_snapshot(filename):
    """
    Lädt eine Ranglisten-Momentaufnahme.
    
    Args:
        filename (str): Pfad zur Ranglisten-Datei
        
    Returns:
        dict: Ranglisten-Daten oder leeres Dict
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Fehler beim Laden der Rangliste: {e}")
        return {}


def save_ranking_history(game, game_id):
    """
    Speichert die komplette Ranglisten-Historie eines Spiels.
    
    Args:
        game (GameRound): Das Spiel
        game_id (str): Eindeutige Spiel-ID
        
    Returns:
        str: Pfad zur Datei
    """
    directory = "resources"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{directory}/ranking_history_{game_id}_{timestamp}.json"
    
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        ranking = Ranking(game.player_scores)
        ranking_list = ranking.get_ranking_with_rank()
        
        history_data = {
            "game_id": game_id,
            "timestamp": datetime.now().isoformat(),
            "total_rounds": game.max_rounds,
            "final_ranking": [
                {
                    "rank": rank,
                    "player": player,
                    "final_score": score
                }
                for rank, player, score in ranking_list
            ],
            "winner": {
                "player": ranking.get_leader()[0],
                "score": ranking.get_leader()[1]
            }
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(history_data, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Ranglisten-Historie in {filename} gespeichert.")
        return filename
    except Exception as e:
        print(f"❌ Fehler beim Speichern der Historie: {e}")
        return None


def get_ranking_files():
    """
    Gibt alle gespeicherten Ranglisten-Dateien zurück.
    
    Returns:
        list: Liste der Datei-Pfade
    """
    directory = "resources"
    if not os.path.exists(directory):
        return []
    
    ranking_files = [f"{directory}/{f}" for f in os.listdir(directory) 
                     if f.startswith("ranking_") and f.endswith(".json")]
    return sorted(ranking_files, reverse=True)


def get_player_ranking_history(player_name):
    """
    Gibt die Ranking-Historie eines bestimmten Spielers.
    
    Args:
        player_name (str): Name des Spielers
        
    Returns:
        list: Liste mit Platzierungen über Zeit
    """
    ranking_files = get_ranking_files()
    history = []
    
    for filename in ranking_files:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                for entry in data.get("ranking", []):
                    if entry["player"] == player_name:
                        history.append({
                            "timestamp": data.get("timestamp"),
                            "rank": entry["rank"],
                            "score": entry["score"]
                        })
        except (FileNotFoundError, json.JSONDecodeError):
            pass
    
    return history


def calculate_ranking_statistics():
    """
    Berechnet Statistiken über alle gespeicherten Ranglisten.
    
    Returns:
        dict: Statistiken (Gewinner, häufigste Positionen, etc.)
    """
    ranking_files = get_ranking_files()
    player_stats = {}
    
    for filename in ranking_files:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                for entry in data.get("ranking", []):
                    player = entry["player"]
                    if player not in player_stats:
                        player_stats[player] = {
                            "total_appearances": 0,
                            "first_places": 0,
                            "total_score": 0,
                            "avg_score": 0
                        }
                    player_stats[player]["total_appearances"] += 1
                    if entry["rank"] == 1:
                        player_stats[player]["first_places"] += 1
                    player_stats[player]["total_score"] += entry["score"]
        except (FileNotFoundError, json.JSONDecodeError):
            pass
    
    # Berechne Durchschnitte
    for player in player_stats:
        if player_stats[player]["total_appearances"] > 0:
            player_stats[player]["avg_score"] = (
                player_stats[player]["total_score"] / 
                player_stats[player]["total_appearances"]
            )
    
    return player_stats
