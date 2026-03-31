import os
import sys
from typing import List, Optional, Callable

# =================================================================
# PFAD-KONFIGURATION (Stellt sicher, dass Module gefunden werden)
# =================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# =================================================================
# IMPORTS AUS DEN ANDEREN LAYERN
# =================================================================
try:
    from domain.GameState_P2_3_4 import GameState, PlayerScore
    from infrastructure.ExtendedGameStorage_P2_3_4 import ExtendedGameStorage
except ModuleNotFoundError as e:
    print(f"❌ Fehler: Module konnten nicht geladen werden. Details: {e}")
    sys.exit(1)

class ExtendedGameApplication:
    """
    Kapselt die Anwendungslogik für das rundenbasierte Würfelspiel.
    Verantwortlich für die Koordination zwischen Domain- und Infrastructure-Layer.
    """
    
    def __init__(self, storage: ExtendedGameStorage):
        """
        Initialisiert die Applikation mit einem Speicher-Manager.
        
        Args:
            storage (ExtendedGameStorage): Instanz für Dateioperationen.
        """
        self.storage = storage
        self.current_game_state: Optional[GameState] = None
    
    def start_new_game(self, player_names: List[str]) -> None:
        """
        Initialisiert einen neuen Spielzustand (Runde 1).
        
        Args:
            player_names (List[str]): Liste der teilnehmenden Spieler.
        """
        player_scores = [PlayerScore(name=name, score=0) for name in player_names]
        self.current_game_state = GameState(
            current_round=1,
            current_player_name=player_names[0],
            player_scores=player_scores,
            timestamp=""
        )
        print(f"\n🎮 Neues Spiel gestartet. Teilnehmer: {', '.join(player_names)}")

    def set_score_for_test(self, player_name: str, points: int):
        """
        Hilfsmethode zum Testen: Erhöht den Punktestand eines Spielers.
        """
        if self.current_game_state:
            for p in self.current_game_state.player_scores:
                if p.name == player_name:
                    p.score += points
                    break

    def complete_round(self) -> None:
        """
        Beendet die aktuelle Runde und triggert das automatische Speichern.
        Inkrementiert danach die Rundenzahl.
        """
        if not self.current_game_state:
            return
        
        round_num = self.current_game_state.current_round
        print(f"\n🏁 Runde {round_num} wurde abgeschlossen.")
        
        # Automatisches Speichern über den Infrastructure-Layer
        filepath = self.storage.auto_save(self.current_game_state)
        print(f"✅ Automatische Sicherung erstellt: {filepath}")
        
        # Zustandsänderung: Nächste Runde vorbereiten
        self.current_game_state.current_round += 1
        print(f"📍 Vorbereitung auf Runde {self.current_game_state.current_round}...")

    def display_standings(self) -> None:
        """
        Gibt die aktuelle Rangliste sortiert in der Konsole aus.
        """
        if not self.current_game_state:
            return
        
        print("\n📊 AKTUELLER SPIELSTAND:")
        print("-" * 35)
        
        # Sortierung: Absteigend nach Punkten
        sorted_players = sorted(
            self.current_game_state.player_scores, 
            key=lambda x: x.score, 
            reverse=True
        )
        
        for p in sorted_players:
            print(f"  👤 {p.name:<15} | {p.score:>3} Punkte")
        print("-" * 35)

# =================================================================
# HAUPTPROGRAMM (EXECUTION BLOCK)
# =================================================================
if __name__ == "__main__":
    # Sicherstellen, dass das Archiv-Verzeichnis existiert
    if not os.path.exists("archive"):
        os.makedirs("archive")

    # 1. Infrastruktur initialisieren
    game_storage = ExtendedGameStorage(storage_path="archive")
    
    # 2. Applikation initialisieren
    app = ExtendedGameApplication(storage=game_storage)
    
    # 3. Test-Szenario ausführen (Mit deutschen Namen)
    print("--- INTEGRATIONSTEST: PERSISTENZ-SYSTEM ---")
    
    # Spiel starten mit deutschen Namen: Lukas, Hanna, Maximilian
    app.start_new_game(["Lukas", "Hanna", "Maximilian"])
    
    # Test-Daten generieren
    app.set_score_for_test("Lukas", 12)
    app.set_score_for_test("Hanna", 25)
    app.set_score_for_test("Maximilian", 18)
    
    # Zwischenstand anzeigen
    app.display_standings()
    
    # Runde beenden & Auto-Save prüfen
    app.complete_round()
    
    print("\n🚀 Testlauf erfolgreich beendet. JSON-Datei im Ordner 'archive' prüfen.")