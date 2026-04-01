#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
  P2.3.5 - Quick Demo Runner (Schnelle Demonstrationsdatei)
  [LERNPFAD: P2.3.1 → P2.3.2 → P2.3.3 → P2.3.4 → P2.3.5 ← AKTUELL]
═══════════════════════════════════════════════════════════════════════════════

📚 ZWECK:
   Diese Datei zeigt P2.3.5 (Siegerehrung) in 3 praktischen Szenarien:
   1. Demo 1: Einfaches Spiel (2 Runden)
   2. Demo 2: Spiel mit Gleichständen (Tie)
   3. Demo 3: Verschiedene Ranking-Szenarien testen

🎯 AUSFÜHRUNG:
   python application/demos/siegerehrung_quick.py

📋 VORBEDINGUNG (aus P2.3.1-4):
   • GameRound initialisiert mit max_rounds
   • GameState mit PlayerScore-Tracking
   • Storage für Auto-Save

💡 LERNZIEL:
   Verstehen wie die finale Siegerehrung mit intelligenter Gleichstand-Verwaltung funktioniert
"""

import os
import sys

# ====================================================================
# PATH SETUP (Subfolder - muss zu Project Root navigieren)
# ====================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
sys.path.insert(0, project_root)

print(f"📁 Demo Pfad: {current_dir}")
print(f"📁 Projekt Root: {project_root}\n")

# ====================================================================
# IMPORTS
# ====================================================================
try:
    print("⏳ Module werden geladen...")
    from domain.FinalRanking_P2_3_5 import FinalRanking
    from application.SiegerehrungApp_P2_3_5 import SiegerehrungApp
    from infrastructure.ExtendedGameStorage_P2_3_4 import ExtendedGameStorage
    print("✅ Alle Module erfolgreich geladen!\n")
except ImportError as e:
    print(f"❌ Fehler beim Import: {e}\n")
    sys.exit(1)


# ====================================================================
# QUICK DEMO 1: BASIC GAME
# ====================================================================
def demo_basic_game():
    """Demo 1: Einfaches Spiel - 2 Runden"""
    print("="*60)
    print("🎮 DEMO 1: Basisspiel (2 Runden)")
    print("="*60)
    
    archive_path = os.path.join(project_root, "archive")
    if not os.path.exists(archive_path):
        os.makedirs(archive_path)
    
    storage = ExtendedGameStorage(storage_path=archive_path)
    app = SiegerehrungApp(storage=storage, max_rounds=2)
    
    players = ["Alice", "Bob", "Charlie"]
    app.start_new_game(players, max_rounds=2)
    
    # Simulate 2 rounds
    for round_num in range(1, 3):
        print(f"\n{'-'*60}")
        print(f"📊 Runde {round_num}:")
        print(f"{'-'*60}")
        
        for player in players:
            app.game_round.execute_player_turn()
            app._sync_game_state()
        
        app.display_standings()
        app.complete_round_and_save()
    
    # Mark game as finished
    app.game_round.game_over = True
    app.game_finished = True
    
    # Final result
    print("\n" + "🎊"*25)
    print("FINALE SIEGEREHRUNG".center(60))
    print("🎊"*25)
    app.display_final_ranking()


# ====================================================================
# QUICK DEMO 2: GLEICHSTAND
# ====================================================================
def demo_gleichstand():
    """Demo 2: Spiel mit Gleichstand"""
    print("\n\n" + "="*60)
    print("🎮 DEMO 2: Spiel mit Gleichstand (Tie)")
    print("="*60)
    
    archive_path = os.path.join(project_root, "archive")
    if not os.path.exists(archive_path):
        os.makedirs(archive_path)
    
    storage = ExtendedGameStorage(storage_path=archive_path)
    app = SiegerehrungApp(storage=storage, max_rounds=1)
    
    players = ["Alice", "Bob", "Charlie", "Diana"]
    app.start_new_game(players, max_rounds=1)
    
    # Manuelle Scores setzen um Gleichstand zu erzeugen
    print("\n📊 Scores (mit Gleichstand):")
    app.game_round.player_scores["Alice"] = 50
    app.game_round.player_scores["Bob"] = 50      # ← Gleichstand!
    app.game_round.player_scores["Charlie"] = 50  # ← 3er-Gleichstand!
    app.game_round.player_scores["Diana"] = 40
    
    for player, score in app.game_round.player_scores.items():
        print(f"  {player}: {score} Punkte")
    
    # Mark game as finished
    app.game_round.game_over = True
    app.game_finished = True
    app._sync_game_state()
    
    # Final result with GLEICHSTAND handling
    print("\n" + "🎊"*25)
    print("FINALE RANGLISTE MIT GLEICHSTAND".center(60))
    print("🎊"*25)
    app.display_final_ranking()


# ====================================================================
# QUICK DEMO 3: TOP3 RANKING TEST
# ====================================================================
def demo_ranking_test():
    """Demo 3: Verschiedene Ranking-Szenarien testen"""
    print("\n\n" + "="*60)
    print("🎮 DEMO 3: RANKING TEST (verschiedene Fälle)")
    print("="*60)
    
    test_cases = [
        {
            "name": "Normal (ohne Gleichstand)",
            "scores": {"Player1": 100, "Player2": 80, "Player3": 60}
        },
        {
            "name": "2er-Gleichstand",
            "scores": {"A": 50, "B": 50, "C": 40}
        },
        {
            "name": "3er-Gleichstand!",
            "scores": {"X": 100, "Y": 100, "Z": 100, "W": 80}
        },
        {
            "name": "Komplex (mehrere Gleichstände)",
            "scores": {"Alice": 60, "Bob": 60, "Charlie": 45, "Diana": 45, "Eve": 30}
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'─'*60}")
        print(f"📋 Test: {test_case['name']}")
        print(f"{'─'*60}")
        
        ranking = FinalRanking(test_case['scores'])
        print(ranking.format_final_ranking_table())


# ====================================================================
# MAIN
# ====================================================================
def main():
    print("\n" + "🎯"*30)
    print("P2.3.5 - SIEGEREHRUNG: QUICK DEMO")
    print("🎯"*30)
    print("\n")
    
    try:
        # Run all demos
        demo_basic_game()
        demo_gleichstand()
        demo_ranking_test()
        
        print("\n\n" + "="*60)
        print("✅ Alle Demos erfolgreich!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
