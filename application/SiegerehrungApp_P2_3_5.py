import os
import sys
import sqlite3
from typing import List, Optional

# Rich Imports
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Path Configuration
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Layer Imports
try:
    from domain.GameState_P2_3_4 import GameState, PlayerScore
    from domain.FinalRanking_P2_3_5 import FinalRanking, RankResult
    from domain.GameRound_P2_3_2 import GameRound
    from infrastructure.ranking_storage_sqlite import SQLiteRankingStorage
    from domain.DiceVisualizer_P2_4_3 import DiceVisualizer
except ModuleNotFoundError as e:
    print(f"❌ Error loading modules: {e}")
    sys.exit(1)

console = Console()

class SiegerehrungApp:
    def __init__(self, db_path: str = "resources/game_results.db", max_rounds: int = 3):
        """Initialisiert die App und die SQLite-Infrastruktur (P2.5.1)."""
        self.max_rounds = max_rounds
        self.game_finished = False
        self.game_round: Optional[GameRound] = None
        self.current_session_id: Optional[int] = None
        
        try:
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            self.connection = sqlite3.connect(db_path)
            self.storage = SQLiteRankingStorage(self.connection)
            self.storage.create_schema()
        except sqlite3.Error as e:
            console.print(f"[bold red]❌ Datenbankfehler:[/bold red] {e}")
            self.storage = None

    def show_lobby(self) -> Optional[int]:
        """Zeigt die Lobby für pausierte Spiele an (P2.5.2)."""
        if not self.storage:
            return None

        sessions = self.storage.get_active_sessions()
        console.print(Panel.fit("[bold magenta]🏟️ SPIELE-LOBBY[/bold magenta]", border_style="magenta"))
        
        if not sessions:
            console.print("[yellow]Keine pausierten Spiele gefunden. Starte neues Turnier...[/yellow]\n")
            return None

        table = Table(title="Verfügbare Spielstände", header_style="bold cyan")
        table.add_column("ID", justify="center")
        table.add_column("Spieler", style="white")
        table.add_column("Runde", justify="center")
        table.add_column("Letztes Update", style="dim")

        for s in sessions:
            table.add_row(str(s[0]), s[1], f"{s[2]}/{s[3]}", s[4])
        
        console.print(table)
        choice = console.input("\n[bold white]Eingabe:[/bold white] ID zum Fortsetzen oder [bold green]'n'[/bold green] für neues Spiel: ")
        
        return int(choice) if choice.isdigit() else None

    def load_existing_game(self, session_id: int) -> bool:
        """Lädt eine Session und stellt den Spielzustand wieder her (P2.5.2)."""
        data = self.storage.get_session_by_id(session_id)
        if data:
            self.current_session_id = session_id
            player_names = data[0].split(", ")
            self.game_round = GameRound(player_names, data[2])
            # Optional: Hier könnten alte Würfe aus dice_rolls geladen werden (P2.5.3)
            console.print(f"[bold green]✅ Spielstand {session_id} geladen.[/bold green]")
            return True
        return False

    def start_new_game(self, player_names: List[str], max_rounds: Optional[int] = None):
        """Initialisiert ein neues Spiel und speichert die Session (P2.5.3)."""
        if max_rounds: self.max_rounds = max_rounds
        self.game_round = GameRound(player_names, self.max_rounds)
        self.game_finished = False
        
        # Session in DB registrieren, um ID für dice_rolls zu erhalten
        if self.storage:
            names_str = ", ".join(player_names)
            self.current_session_id = self.storage.save_session(names_str, 1, self.max_rounds)
        
        console.print(Panel.fit("[bold cyan]🎲 WÜRFELSPIEL START[/bold cyan]\n"
                                f"Modus: {self.max_rounds} Runden", border_style="blue"))

    def execute_player_turn(self) -> dict:
        """Führt einen Zug aus und sichert den Wurf sofort (P2.5.3)."""
        if not self.game_round or self.game_finished: return {}
        
        turn_result = self.game_round.execute_player_turn()
        
        # Sofortige Speicherung des Wurfs (Lückenlose Aufzeichnung)
        if self.storage and self.current_session_id:
            self.storage.save_roll(
                self.current_session_id, 
                turn_result['player'], 
                turn_result['dice_result']
            )
        
        console.print(f"\n👤 [bold white]{turn_result['player']}[/bold white] würfelt...")
        dice_art = DiceVisualizer.get_dice_art(turn_result['dice_result'])
        for line in dice_art:
            console.print(f"   [bold yellow]{line}[/bold yellow]")
            
        console.print(f"   Ergebnis: [bold]{turn_result['dice_result']}[/bold] | "
                      f"Gesamt: [green]{turn_result['total_score']}[/green]")
        
        if self.game_round.game_over:
            self._handle_game_end()
            
        return turn_result

    def _handle_game_end(self):
        """Verarbeitet das Spielende und speichert das finale Ranking."""
        self.game_finished = True
        console.print("\n[bold green]🏁 Spielende erreicht! Speichere Ergebnisse...[/bold green]")
        
        scores_dict = {p if isinstance(p, str) else p.name: 
                       self.game_round.player_scores.get(p if isinstance(p, str) else p.name, 0) 
                       for p in self.game_round.players}

        final_ranking_logic = FinalRanking(scores_dict)
        results = final_ranking_logic.get_final_ranking_with_ties()
        
        if self.storage:
            for res in results:
                self.storage.save_result(res)
            console.print("[bold green]✅ Ergebnisse wurden in SQLite gespeichert.[/bold green]")
        
        self.display_final_results(results)

    def display_final_results(self, results: List[RankResult]):
        """Visualisiert das finale Ranking mit Rich."""
        table = Table(title="🏆 FINAL RANKING", header_style="bold magenta")
        table.add_column("Rang", justify="center")
        table.add_column("Spieler", style="white")
        table.add_column("Punkte", justify="right", style="green")

        for res in results:
            table.add_row(str(res.rank), res.player_name, str(res.score))
        
        console.print(table)

    def __del__(self):
        """Schließt die Datenbankverbindung beim Beenden der App."""
        if hasattr(self, 'connection'):
            self.connection.close()

if __name__ == "__main__":
    db_file = os.path.join(project_root, "resources", "game_results.db")
    app = SiegerehrungApp(db_path=db_file)
    
    selected_id = app.show_lobby()
    
    if selected_id:
        if not app.load_existing_game(selected_id):
            app.start_new_game(["Lukas", "Hanna"], max_rounds=2)
    else:
        app.start_new_game(["Lukas", "Hanna"], max_rounds=2)
    
    # Beispielhafte Züge
    app.execute_player_turn()
    app.execute_player_turn()