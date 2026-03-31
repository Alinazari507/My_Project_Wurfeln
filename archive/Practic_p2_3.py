def get_number_of_players():
    """
    Fragt den Benutzer nach der Anzahl der Spieler (1-99).
    Validiert, ob die Eingabe eine Zahl im erlaubten Bereich ist.
    """
    while True:
        eingabe = input("Anzahl der Spieler eingeben (1-99): ").strip()
        
        # Prüfen, ob die Eingabe nur aus Ziffern besteht
        if eingabe.isdigit():
            anzahl = int(eingabe)
            # Prüfen, ob die Zahl im Bereich 1 bis 99 liegt
            if 1 <= anzahl <= 99:
                return anzahl  # Gibt den validierten Wert zurück
            else:
                print("❌ Fehler: Die Zahl muss zwischen 1 und 99 liegen.")
        else:
            print("❌ Fehler: Bitte nur Zahlen eingeben (keine Buchstaben oder Sonderzeichen).")
def get_plazyer_name (spieler_name):
    while True:
        name = input(f"name für Spieler{spieler_name} eingaben: ").strip()
        if name.isalph():
            return name
        