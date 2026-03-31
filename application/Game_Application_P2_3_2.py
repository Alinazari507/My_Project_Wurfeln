import sys
import os

# Pfad zum Hauptverzeichnis hinzufügen
sys.path.append(os.getcwd())

from domain.player_management_P2_3_1 import get_number_of_players, get_player_name
from domain.GameRound_P2_3_2 import GameRound

def get_round_limit():
    while True:
        try:
            eingabe = input("Wie viele Runden soll das Spiel dauern? (1-99): ").strip()
            runden = int(eingabe)
            if 1 <= runden <= 99:
                return runden
            print("❌ Bitte eine Zahl zwischen 1 und 99 eingeben.")
        except ValueError:
            print("❌ Ungültige Eingabe! Bitte eine Zahl eingeben.")

def display_game_status(game):
    status = game.get_game_status()
    print("\n" + "═" * 40)
    print(f" 🚩 RUNDE {status['round']} von {status['max_rounds']}")
    print(f" 👉 Dran ist: {status['current_player']}")
    print(" " + "─" * 39)
    for player, score in status['scores'].items():
        prefix = "⭐ " if player == status['current_player'] else "  "
        print(f" {prefix}{player:.<15} {score:>2} Punkte")
    print("═" * 40)

def run_game():
    print("🎲 WILLKOMMEN ZUM RUNDENBASIERTEN WÜRFELSPIEL")
    
    # Setup
    anzahl = get_number_of_players()
    spieler = [get_player_name(i) for i in range(1, anzahl + 1)]
    runden = get_round_limit()
    
    game = GameRound(spieler, runden)
    
    # Game Loop
    while not game.game_over:
        display_game_status(game)
        input(f"\n{game.get_current_player()}, [ENTER] zum Würfeln...")
        
        result = game.execute_player_turn()
        print(f"🎲 Ergebnis: {result['dice_result']} | Gesamt: {result['total_score']}")
        
    # Finale
    print("\n🏆 ENDERGEBNISSE:")
    for rank, (name, score) in enumerate(game.get_final_scores(), 1):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."
        print(f"{medal} {name}: {score} Punkte")

if __name__ == "__main__":
    run_game()