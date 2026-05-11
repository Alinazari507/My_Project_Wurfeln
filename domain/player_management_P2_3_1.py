import re

"""
DOMAIN LAYER: Player Management
Dieses Modul enthält die reine Geschäftslogik für die Spieler-Validierung.
Es gibt hier keine Inputs oder Prints, da dies die Aufgabe der Application-Layer ist.
"""

def validate_player_count(anzahl_str):
    """
    Prüft, ob die Spieleranzahl eine gültige Zahl zwischen 1 und 99 ist.
    
    Args:
        anzahl_str (str/int): Die vom Benutzer eingegebene Anzahl.
        
    Returns:
        int: Die validierte Anzahl als Integer.
        
    Raises:
        ValueError: Wenn die Eingabe keine Zahl ist oder außerhalb des Bereichs liegt.
    """
    try:
        anzahl = int(anzahl_str)
        if 1 <= anzahl <= 99:
            return anzahl
        # Wenn die Zahl außerhalb des Bereichs liegt
        raise ValueError("Die Anzahl der Spieler muss zwischen 1 und 99 liegen.")
    except (ValueError, TypeError):
        # Wenn die Umwandlung in int scheitert
        raise ValueError("Ungültige Eingabe! Bitte geben Sie eine Ganzzahl ein.")


def validate_player_name(name):
    """
    Validiert den Namen gegen ein RegEx-Muster.
    Erlaubt Buchstaben (inkl. Umlaute), Leerzeichen und Bindestriche.
    
    Args:
        name (str): Der zu prüfende Name.
        
    Returns:
        str: Der bereinigte und validierte Name.
        
    Raises:
        ValueError: Wenn der Name leer ist oder ungültige Zeichen enthält.
    """
    # RegEx-Pattern: Buchstaben, deutsche Umlaute, Leerzeichen und Bindestriche
    pattern = r"^[a-zA-ZäöüßÄÖÜ\s\-]+$"
    
    if not name:
        raise ValueError("Der Name darf nicht leer sein.")
        
    name = name.strip()
    
    if re.match(pattern, name):
        return name
    else:
        raise ValueError(f"Der Name '{name}' ist ungültig (nur Buchstaben erlaubt).")


if __name__ == "__main__":
    # Kleiner interner Testbereich (Unit Test Light)
    try:
        print(f"Test 1 (Zahl 5): {validate_player_count('5')}")
        print(f"Test 2 (Name 'Max'): {validate_player_name('Max')}")
        # Test 3 soll absichtlich einen Fehler werfen:
        # print(f"Test 3 (Fehler): {validate_player_count('abc')}")
    except ValueError as e:
        print(f"Test-Fehler abgefangen: {e}")