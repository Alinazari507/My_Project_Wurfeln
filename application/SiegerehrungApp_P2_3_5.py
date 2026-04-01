import os
import sys
from typing import List, Optional, Dict

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
try:
    from domain.GameState_P2_3_4 import GameState, PlayerScore
    from domain.FinalRanking_P2_3_5 import FinalRanking, RankResult
    from domain.GameRound_P2_3_2 import GameRound
    from infrastructure.ExtendedGameStorage_P2_3_4 import ExtendedGameStorage
except ModuleNotFoundError as e:
    print(f"❌ Fehler beim Laden der Module: {e}")
    sys.exit(1)


class SiegerehrungApp:
    """
    Zentrale Anwendungslogik für das Spiel inklusive der finalen Siegerehrung.
    Koordiniert den Spielablauf, die Persistierung und das Ranking.
    """
    
    def __init__(self, storage: Optional[ExtendedGameStorage] = None, max_rounds: int = 3):
        """
        Initialisiert die Applikation mit optionalem Speicher-Manager.
        """
        self.storage = storage
        self.max_rounds = max_rounds
        self.current_game_state: Optional[GameState] = None
        self.game_round: Optional[GameRound] = None
        self.game_finished = False
        self.final_ranking: Optional[FinalRanking] = None
    
    def start_new_game(self, player_names: List[str], max_rounds: Optional[int] = None) -> None:
        """
        Startet eine neue Spielinstanz und initialisiert den Spielzustand.
        """
        if not player_names:
            print("❌ Fehler: Keine Spieler angegeben.")
            return
        
        if max_rounds:
            self.max_rounds = max_rounds
        
        # Initialisierung des GameStates
        scores = [PlayerScore(name=name, score=0) for name in player_names]
        self.current_game_state = GameState(
            current_round=1,
            current_player_name=player_names[0],
            player_scores=scores,
            timestamp=""
        )
        
        self.game_round = GameRound(player_names, self.max_rounds)
        self.game_finished = False
        self.final_ranking = None
        
        print(f"\n{'🎮' * 20}")
        print(" SPIEL GESTARTET ".center(40, " "))
        print(f"{'🎮' * 20}")
        print(f"👥 Spieler: {', '.join(player_names)}")
        print(f"⏳ Runden: {self.max_rounds}\n")
    
    def execute_player_turn(self) -> dict:
        """
        Führt den nächsten Spielzug aus und synchronisiert den Status.
        """
        if not self.game_round or self.game_finished:
            return {}
        
        turn_result = self.game_round.execute_player_turn()
        self._sync_game_state()
        
        print(f"🎲 {turn_result['player']} würfelt eine {turn_result['dice_result']}!")
        print(f"   Aktueller Punktestand: {turn_result['total_score']}")
        
        if self.game_round.game_over:
            self.game_finished = True
            print("\n🏁 Das Spiel ist beendet!")
            
        return turn_result
    
    def complete_round_and_save(self) -> None:
        """
        Schließt die aktuelle Runde ab und führt ein Auto-Save durch.
        """
        if not self.current_game_state:
            return
        
        print(f"\n📍 Runde {self.current_game_state.current_round} abgeschlossen.")
        
        if self.storage:
            path = self.storage.auto_save(self.current_game_state)
            print(f"💾 Automatische Speicherung unter: {path}")
    
    def display_final_ranking(self) -> None:
        """
        Führt die finale Siegerehrung durch (Akzeptanzkriterium P2.3.5).
        """
        if not self.game_finished or not self.current_game_state:
            print("❌ Siegerehrung erst nach Spielende möglich.")
            return
        
        # Initialisierung des Ranking-Service mit aktuellen Scores
        self.final_ranking = FinalRanking(self.current_game_state.player_scores)
        
        # Ausgabe der formatierten Tabelle und des Podiums
        print(self.final_ranking.format_final_ranking_table())
        self.final_ranking.display_podium()
        
        winners = self.final_ranking.get_winner()
        if len(winners) == 1:
            print(f"🏆 DER GEWINNER IST: {winners[0]}! 🏆\n")
        else:
            print(f"🏆 GLEICHSTAND! GEWINNER SIND: {', '.join(winners)}! 🏆\n")
    
    def _sync_game_state(self) -> None:
        """
        Abgleich zwischen der Spiellogik (GameRound) und dem Zustand (GameState).
        """
        if not self.game_round or not self.current_game_state:
            return
        
        # Scores im GameState aktualisieren
        for ps in self.current_game_state.player_scores:
            ps.score = self.game_round.player_scores[ps.name]
        
        self.current_game_state.current_round = self.game_round.current_round
        self.current_game_state.current_player_name = self.game_round.get_current_player()


# =================================================================
# DEMO-MODUS
# =================================================================
if __name__ == "__main__":
    # Vorbereitung der Umgebung
    if not os.path.exists("archive"):
        os.makedirs("archive")
    
    game_storage = ExtendedGameStorage(storage_path="archive")
    app = SiegerehrungApp(storage=game_storage, max_rounds=2)
    
    # Test-Szenario: Gleichstand-Demonstration
    players = ["Lukas", "Hanna", "Sarah"]
    app.start_new_game(players, max_rounds=1)
    
    # Simulation der Würfe (Manuelle Score-Setzung für Demo-Zwecke)
    # In einem echten Spiel würde execute_player_turn() genutzt werden
    app.game_round.player_scores["Lukas"] = 15
    app.game_round.player_scores["Hanna"] = 15  # Gleichstand Gold
    app.game_round.player_scores["Sarah"] = 10  # Bronze
    
    # Spielabschluss simulieren
    app.game_round.game_over = True
    app.game_finished = True
    app._sync_game_state()
    
    # FINALE SIEGEREHRUNG
    app.display_final_ranking()