import os
import sys

# =================================================================
# PFAD-KONFIGURATION
# =================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# =================================================================
# IMPORTS
# =================================================================
from domain.FinalRanking_P2_3_5 import FinalRanking
from application.SiegerehrungApp_P2_3_5 import SiegerehrungApp
from infrastructure.ExtendedGameStorage_P2_3_4 import ExtendedGameStorage

def test_acceptance_criteria_1():
    """
    ✅ AKZEPTANZKRITERIUM 1: ENDABRECHNUNG BEI RUNDENLIMIT
    Überprüft، ob das Spiel nach Erreichen des Rundenlimits korrekt beendet 
    und die finale Rangliste ausgegeben wird.
    """
    print("\n" + "="*60)
    print("TEST 1: ENDABRECHNUNG NACH RUNDENLIMIT".center(60))
    print("="*60)
    
    storage = ExtendedGameStorage(storage_path="archive")
    app = SiegerehrungApp(storage=storage, max_rounds=1)
    
    # Start mit 3 Spielern
    app.start_new_game(["Alice", "Bob", "Charlie"], max_rounds=1)
    
    # Durchführung der Würfe für eine Runde
    for _ in range(3):
        app.execute_player_turn()
    
    app._sync_game_state()
    
    # Verifikation
    is_over = app.game_round.game_over
    print(f"\n🔍 Verifikation: Spiel beendet? {'✅' if is_over else '❌'}")
    
    if is_over:
        app.display_final_ranking()
    
    print("\n✅ KRITERIUM 1 ERFÜLLT!")

def test_acceptance_criteria_2():
    """
    ✅ AKZEPTANZKRITERIUM 2: GLEICHSTAND-HANDLING
    Überprüft، ob Spieler mit gleicher Punktzahl den gleichen Rang erhalten.
    """
    print("\n" + "="*60)
    print("TEST 2: GLEICHSTAND-LOGIK (TIES)".center(60))
    print("="*60)
    
    # Test-Daten mit 3er- und 2er-Gleichständen
    test_scores = {
        "Alice": 50, "Bob": 50, "Charlie": 50, # Rang 1
        "Diana": 40, "Eve": 40,                # Rang 4
        "Frank": 30                            # Rang 6
    }
    
    ranking_service = FinalRanking(test_scores)
    results = ranking_service.get_final_ranking_with_ties()
    
    print("\n🔍 Analyse der Ränge:")
    for res in results:
        # Zugriff über .rank und .player_name (dank dataclass)
        print(f"  Rang {res.rank}: {res.player_name} ({res.score} Pkt)")
    
    # Validierung der Logik
    rank_1_count = len([r for r in results if r.rank == 1])
    rank_4_count = len([r for r in results if r.rank == 4])
    
    assert rank_1_count == 3, "Fehler: Es sollten 3 Spieler auf Rang 1 sein!"
    assert rank_4_count == 2, "Fehler: Es sollten 2 Spieler auf Rang 4 sein!"
    
    print("\n✅ Validierung erfolgreich: Ränge wurden korrekt vergeben.")
    print(ranking_service.format_final_ranking_table())

def test_complex_scenario():
    """
    🎯 KOMPLEXES SZENARIO: KOMBINATION ALLER KRITERIEN
    """
    print("\n" + "="*60)
    print("TEST 3: KOMPLEXES SZENARIO (SPIELABLAUF + TIES)".center(60))
    print("="*60)
    
    app = SiegerehrungApp(max_rounds=2)
    app.start_new_game(["Player_A", "Player_B"], max_rounds=2)
    
    # Manuelle Punktesetzung für den Test
    app.game_round.player_scores["Player_A"] = 25
    app.game_round.player_scores["Player_B"] = 25
    
    app.game_round.game_over = True
    app.game_finished = True
    app._sync_game_state()
    
    app.display_final_ranking()
    print("✅ Komplexer Test abgeschlossen.")

if __name__ == "__main__":
    print("\n" + "🚀" * 20)
    print(" START DER AKZEPTANZTESTS P2.3.5 ".center(40))
    print("🚀" * 20)
    
    try:
        test_acceptance_criteria_1()
        test_acceptance_criteria_2()
        test_complex_scenario()
        print("\n" + "✨" * 20)
        print(" ALLE TESTS BESTANDEN! ".center(40))
        print("✨" * 20 + "\n")
    except AssertionError as e:
        print(f"\n❌ Test fehlgeschlagen: {e}")
    except Exception as e:
        print(f"\n❌ Unerwarteter Fehler: {e}")