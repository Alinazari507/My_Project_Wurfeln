import re

def get_number_of_players():
    """
    Fragt den Benutzer nach der Anzahl der Spieler (1-99).
    Verwendet eine Fehlerbehandlung (Try-Except), um ungültige Eingaben abzufangen.
    
    Returns:
        int: Die validierte Anzahl der Spieler.
    """
    while True:
        eingabe = input("Anzahl der Spieler eingeben (1-99): ").strip()
        
        try:
            # Versuch, die Eingabe in eine Ganzzahl umzuwandeln
            anzahl = int(eingabe)
            if 1 <= anzahl <= 99:
                return anzahl
            else:
                print("❌ Fehler: Bitte eine Zahl zwischen 1 und 99 eingeben.")
        except ValueError:
            # Wird ausgeführt, wenn die Umwandlung in int() scheitert
            print("❌ Fehler: Ungültige Eingabe! Bitte nur Zahlen eingeben.")

def get_player_name(spieler_nummer):
    """
    Validiert den Spielernamen mithilfe von RegEx.
    Erlaubt Buchstaben (inkl. Umlaute), Leerzeichen und Bindestriche.
    
    Args:
        spieler_nummer (int): Die Nummer des aktuellen Spielers für die Anzeige.
        
    Returns:
        str: Der validierte Name des Spielers.
    """
    # RegEx-Pattern: Erlaubt A-Z, a-z, deutsche Umlaute (äöüß), Leerzeichen und Bindestriche
    pattern = r"^[a-zA-ZäöüßÄÖÜ\s\-]+$"
    
    while True:
        name = input(f"Name für Spieler {spieler_nummer} eingeben: ").strip()
        
        # Sicherstellen, dass die Eingabe nicht leer ist
        if not name:
            print("❌ Fehler: Der Name darf nicht leer sein.")
            continue
            
        # Überprüfung des Namens gegen das definierte Muster
        if re.match(pattern, name):
            return name
        else:
            print(f"❌ Fehler: '{name}' ist ungültig. (Nur Buchstaben, Leerzeichen oder Bindestriche erlaubt).")

if __name__ == "__main__":
    # Test-Bereich für die Validierung der Logik
    print("--- SETUP TEST-MODUS ---")
    anzahl = get_number_of_players()
    
    spieler_liste = []
    for i in range(1, anzahl + 1):
        name = get_player_name(i)
        spieler_liste.append(name)
    
    print(f"\n✅ Setup erfolgreich für: {', '.join(spieler_liste)}")