import sys
import os

# Pfad-Konfiguration für die Layer-Struktur
sys.path.append(os.getcwd())

from domain.player_management_P2_3_1 import get_number_of_players, get_player_name
from infrastructure.data_storage_P2_3_1 import save_players

def run_setup():
    """
    Hauptablauf für User Story P2.3.1: Setup der Spieler.
    """
    print("=" * 40)
    print("🎲 WÜRFELSPIEL - SETUP-MODUS")
    print("=" * 40)

    # 1. Logik aus Domain aufrufen
    anzahl = get_number_of_players()
    
    # 2. Namen sammeln
    spieler_liste = []
    for i in range(1, anzahl + 1):
        name = get_player_name(i)
        spieler_liste.append(name)

    # 3. In Infrastructure speichern
    save_players(spieler_liste)

    print("\n✅ Setup beendet. Viel Erfolg beim Spiel!")

if __name__ == "__main__":
    run_setup()