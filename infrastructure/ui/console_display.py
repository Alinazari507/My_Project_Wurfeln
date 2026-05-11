# infrastructure/console_display.py
from rich.console import Console
from rich.panel import Panel

class ConsoleDisplay:
    """
    Diese Klasse verwaltet die farbige Textausgabe in der Konsole 
    unter Verwendung der 'rich' Bibliothek.
    """

    def __init__(self):
        # Initialisiert die rich-Konsole für die Ausgabe
        self.console = Console()

    def show_welcome(self, message):
        """
        Zeigt eine Willkommensnachricht in einem grünen Rahmen an.
        """
        self.console.print(Panel(f"[bold green]{message}[/bold green]", expand=False))

    def show_error(self, message):
        """
        Gibt eine Fehlermeldung in fettgedrucktem Rot aus.
        """
        self.console.print(f"[bold red]❌ Fehler:[/bold red] {message}")

    def show_success(self, message):
        """
        Bestätigt eine erfolgreiche Aktion in Grün.
        """
        self.console.print(f"[bold green]✔[/bold green] {message}")

    def show_info(self, message):
        """
        Gibt allgemeine Informationen in Blau aus.
        """
        self.console.print(f"[bold blue]ℹ️ Info:[/bold blue] {message}")