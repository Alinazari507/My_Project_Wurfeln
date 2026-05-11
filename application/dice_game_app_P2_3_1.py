import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt

# Pfad-Konfiguration
sys.path.append(os.getcwd())

# Import der professionellen Logik aus den anderen Schichten
from domain.player_management_P2_3_1 import validate_player_name
from infrastructure.data_storage_P2_3_1 import save_players

console = Console()

def run_setup():
    """
    Hauptablauf für das Spieler-Setup (P2.4) mit Rich-UI.
    """
    console.clear()
    
    # 🎨 Visueller Header
    console.print(Panel.fit(
        "[bold cyan]🎲 WÜRFELSPIEL - SETUP-MODUS[/bold cyan]", 
        border_style="blue", 
        subtitle="Clean Code & Rich UI"
    ))

    # 1. Anzahl der Spieler abfragen
    # Rich kümmert sich intern um die Validierung der Auswahl
    anzahl = IntPrompt.ask(
        "[bold yellow]Wie viele Spieler nehmen teil?[/bold yellow]", 
        choices=["2", "3", "4"], # Beispiel für eine Auswahl
        default=2
    )
    
    # 2. Namen sammeln und über Domain validieren
    spieler_liste = []
    for i in range(1, anzahl + 1):
        while True:
            name_eingabe = Prompt.ask(f"[cyan]Name für Spieler {i}[/cyan]")
            try:
                # Validierung in der Domain-Schicht
                valid_name = validate_player_name(name_eingabe)
                spieler_liste.append(valid_name)
                break 
            except ValueError as e:
                # ❌ Fehleranzeige in Rot (User Story Anforderung)
                console.print(f"[bold red]❌ {str(e)}[/bold red]")

    # 3. Speichern über Infrastructure
    try:
        if save_players(spieler_liste):
            # ✅ Erfolgsmeldung in Grün
            console.print(f"\n[bold green]✔ Die Spielerliste wurde sicher in 'resources/' gespeichert.[/bold green]")
    except Exception as e:
        console.print(f"\n[bold red]❌ KRITISCHER FEHLER: {str(e)}[/bold red]")

    # Abschluss-Panel
    console.print(Panel(
        f"[bold white]Bereit zum Spielen![/bold white]\n[yellow]Teilnehmer: {', '.join(spieler_liste)}[/yellow]",
        title="[bold green]Setup Abgeschlossen[/bold green]",
        border_style="green"
    ))

if __name__ == "__main__":
    run_setup()