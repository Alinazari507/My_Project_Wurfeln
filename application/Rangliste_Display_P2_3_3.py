import sys
import os
sys.path.append(os.getcwd())

from domain.Ranking_P2_3_3 import Ranking


def display_ranking(game):
    """
    Zeigt die aktuelle Rangliste nach einer vollständigen Runde an.
    
    Akzeptanzkriterium:
    GEGEBEN eine Spielrunde wurde von allen Spieler*innen beendet
    WENN die nächste Spielrunde beginnt
    DANN wird am Anfang die aktuelle Rangliste der Spieler*innen nach Punkten absteigend angezeigt
    
    Args:
        game (GameRound): Das aktuelle Spiel mit player_scores
    """
    ranking = Ranking(game.player_scores)
    ranking_list = ranking.get_ranking_with_rank()
    
    print("\n" + "=" * 70)
    print("  📊 RANGLISTE NACH RUNDE " + str(game.current_round - 1))
    print("=" * 70)
    
    # Tabellen-Header
    print(f"  {'Platz':<6} {'Spieler*in':<25} {'Punkte':<10} {'Status':<10}")
    print("  " + "-" * 66)
    
    # Ranglisten-Einträge
    medals = ["🥇", "🥈", "🥉"]
    for rank, player, score in ranking_list:
        medal = medals[rank - 1] if rank <= 3 else "  "
        
        # Status mit Pfeilen
        if rank == 1:
            status = "🔝 Führend"
        elif rank == len(ranking_list):
            status = "📉 Letzter"
        else:
            status = f"#{rank}"
        
        print(f"  {medal} {rank}. {player:<22} {score:<10} {status}")
    
    print("=" * 70 + "\n")


def display_ranking_detailed(game):
    """
    Zeigt eine detaillierte Rangliste mit zusätzlichen Informationen.
    
    Args:
        game (GameRound): Das aktuelle Spiel
    """
    ranking = Ranking(game.player_scores)
    ranking_list = ranking.get_ranking()
    top_3 = ranking.get_top_3()
    leader, leader_score = ranking.get_leader()
    
    print("\n" + "=" * 70)
    print("  📊 DETAILLIERTE RANGLISTE - RUNDE " + str(game.current_round - 1))
    print("=" * 70)
    
    # TOP 3 HIGHLIGHT
    if top_3:
        print("\n  🏆 TOP 3 SPIELER*INNEN:")
        print("  " + "-" * 66)
        medals = ["🥇", "🥈", "🥉"]
        for idx, (player, score) in enumerate(top_3):
            medal = medals[idx]
            percentage = (score / max([s for _, s in ranking_list]) * 100) if ranking_list else 0
            bar = "█" * int(percentage / 5) + "░" * (20 - int(percentage / 5))
            print(f"  {medal} {player:<20} {score:>4} Punkte  [{bar}] {percentage:.0f}%")
    
    # ALLE SPIELER
    print("\n  📋 ALLE SPIELER*INNEN (SORTIERT):")
    print("  " + "-" * 66)
    for rank, (player, score) in enumerate(ranking_list, 1):
        symbol = "→ " if player == leader else "  "
        print(f"  {symbol}{rank:2}. {player:<25} {score:>5} Punkte")
    
    # STATISTIK
    print("\n  📈 STATISTIK:")
    print("  " + "-" * 66)
    if ranking_list:
        all_scores = [score for _, score in ranking_list]
        print(f"  🔝 Führung: {leader} mit {leader_score} Punkten")
        print(f"  📊 Durchschnitt: {sum(all_scores) / len(all_scores):.1f} Punkte")
        print(f"  📈 Rangabstand: {all_scores[0] - all_scores[-1]} Punkte (Top vs. Last)")
    
    print("=" * 70 + "\n")


def display_round_transition(game):
    """
    Zeigt den Übergang zwischen Runden mit Rangliste.
    Wird aufgerufen WENN eine Runde endet und die nächste beginnt.
    
    Args:
        game (GameRound): Das aktuelle Spiel
    """
    print("\n" + "=" * 70)
    print("  ✅ RUNDE " + str(game.current_round - 1) + " BEENDET!")
    print("=" * 70)
    
    # Zeige Rangliste
    display_ranking(game)
    
    # Nächste Runde Ankündigung
    if not game.game_over:
        print(f"  ⏭️  Starte RUNDE {game.current_round}...")
        print("  " + "-" * 66)
        print(f"  👤 Erster Spieler: {game.get_current_player()}")
        print("=" * 70)
        input("\n  Drücke [ENTER] um die nächste Runde zu starten...")


def display_game_end_rankings(game):
    """
    Zeigt die finale Rangliste am Ende des Spiels.
    
    Args:
        game (GameRound): Das beendete Spiel
    """
    ranking = Ranking(game.player_scores)
    ranking_list = ranking.get_ranking_with_rank()
    
    print("\n" + "=" * 70)
    print("  🎉 FINAL-RANGLISTE 🎉")
    print("=" * 70)
    
    medals = ["🥇", "🥈", "🥉"]
    for rank, player, score in ranking_list:
        medal = medals[rank - 1] if rank <= 3 else "  "
        
        # Distinktion für Platzierungen
        if rank == 1:
            distinction = " ⭐ GEWINNER*IN ⭐"
        elif rank == 2:
            distinction = " 👏 2. Platz"
        elif rank == 3:
            distinction = " 😊 3. Platz"
        else:
            distinction = ""
        
        print(f"  {medal} {rank}. {player:<25} {score:>5} Punkte{distinction}")
    
    print("=" * 70 + "\n")


# ============ TEST SIMULATION ============

if __name__ == "__main__":
    """
    Test-Beispiel zur Demonstration der Ranglisten-Funktionen
    """
    from domain.GameRound_P2_3_2 import GameRound
    
    # Test-Spieler und Scores
    players = ["Alice", "Bob", "Charlie", "Diana"]
    game = GameRound(players, 3)
    
    # Simuliere einige Würfelwürfe
    game.player_scores["Alice"] = 15
    game.player_scores["Bob"] = 12
    game.player_scores["Charlie"] = 18
    game.player_scores["Diana"] = 10
    
    print("🧪 TEST: Ranglisten-Anzeige\n")
    
    # Test 1: Einfache Rangliste
    print("1️⃣  EINFACHE RANGLISTE:")
    display_ranking(game)
    
    # Test 2: Detaillierte Rangliste
    print("2️⃣  DETAILLIERTE RANGLISTE:")
    display_ranking_detailed(game)
    
    # Test 3: Final-Rangliste
    print("3️⃣  FINAL-RANGLISTE:")
    game.game_over = True
    display_game_end_rankings(game)
