import os
import sys
import traceback

# ====================================================================
# SYSTEM-SETUP
# ====================================================================
# Stellt sicher, dass das aktuelle Verzeichnis im Python-Pfad ist
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# ====================================================================
# IMPORTS
# ====================================================================
try:
    from application.SiegerehrungApp_P2_3_5 import SiegerehrungApp
    from infrastructure.ExtendedGameStorage_P2_3_4 import ExtendedGameStorage
    # Test-Importe werden erst bei Bedarf in run_tests() geladen
except ImportError as e:
    print(f"❌ Kritischer Fehler beim Laden der Komponenten: {e}")
    sys.exit(1)

# ====================================================================
# HILFSFUNKTIONEN
# ====================================================================

def clear_screen():
    """Löscht den Terminal-Inhalt (Plattformübergreifend)."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Gibt einen einheitlichen Header für die Menüpunkte aus."""
    print("\n" + "═" * 60)
    print(f" {title} ".center(60, "═"))
    print("═" * 60 + "\n")

# ====================================================================
# MENÜ-AKTIONEN
# ====================================================================

def demo_default():
    """Demo 1: Standard-Spielablauf mit 3 Spielern."""
    print_header("DEMO: STANDARD-SPIEL (2 RUNDEN)")
    
    app = SiegerehrungApp(max_rounds=2)
    players = ["Alice", "Bob", "Charlie"]
    app.start_new_game(players)
    
    for round_num in range(1, 3):
        print(f"📍 STARTE RUNDE {round_num}...")
        for _ in players:
            app.execute_player_turn()
        app.complete_round_and_save()
    
    app.display_final_ranking()

def demo_gleichstand():
    """Demo 2: Gezielte Demonstration von Gleichständen."""
    print_header("DEMO: GLEICHSTAND-HANDLING")
    
    app = SiegerehrungApp(max_rounds=1)
    app.start_new_game(["Lukas", "Hanna", "Sarah"])
    
    # Manuelle Manipulation für Demo-Zwecke
    print("ℹ️ Setze Scores manuell auf Gleichstand (Lukas & Hanna: 50 Pkt)...")
    app.game_round.player_scores["Lukas"] = 50
    app.game_round.player_scores["Hanna"] = 50
    app.game_round.player_scores["Sarah"] = 40
    
    app.game_round.game_over = True
    app.game_finished = True
    app._sync_game_state()
    
    app.display_final_ranking()

def demo_custom():
    """Demo 3: Benutzerdefiniertes Spiel mit Eingabe."""
    print_header("DEMO: BENUTZERDEFINIERTES SPIEL")
    
    try:
        names_raw = input("Spielernamen eingeben (kommagetrennt): ")
        players = [n.strip() for n in names_raw.split(",") if n.strip()]
        
        if len(players) < 2:
            print("❌ Fehler: Mindestens 2 Spieler erforderlich.")
            return
            
        rounds = int(input("Anzahl der Runden: "))
        
        app = SiegerehrungApp(max_rounds=rounds)
        app.start_new_game(players)
        
        while not app.game_finished:
            app.execute_player_turn()
            
        app.display_final_ranking()
        
    except ValueError:
        print("❌ Fehler: Ungültige Eingabe bei der Rundenanzahl.")

def run_all_tests():
    """Führt die Akzeptanztests aus dem Testmodul aus."""
    print_header("SYSTEM-TESTS (P2.3.5)")
    try:
        from application.Akzeptanztest_P2_3_5 import (
            test_acceptance_criteria_1,
            test_acceptance_criteria_2,
            test_complex_scenario
        )
        test_acceptance_criteria_1()
        test_acceptance_criteria_2()
        test_complex_scenario()
        print("\n✅ Alle System-Tests erfolgreich abgeschlossen.")
    except ImportError:
        print("❌ Fehler: Test-Modul 'Akzeptanztest_P2_3_5' nicht gefunden.")

# ====================================================================
# MAIN LOOP
# ====================================================================

def main():
    """Hauptmenü-Schleife."""
    while True:
        clear_screen()
        print_header("🏆 P2.3.5 - WÜRFELSPIEL SIEGEREHRUNG 🏆")
        print(" [1] Standard-Demo (2 Runden)")
        print(" [2] Gleichstand-Demo (Spezialfall)")
        print(" [3] Eigenes Spiel starten")
        print(" [4] Akzeptanztests ausführen")
        print(" [5] Beenden")
        print("\n" + "═" * 60)
        
        wahl = input("\nIhre Wahl (1-5): ").strip()
        
        if wahl == "1":
            demo_default()
        elif wahl == "2":
            demo_gleichstand()
        elif wahl == "3":
            demo_custom()
        elif wahl == "4":
            run_all_tests()
        elif wahl == "5":
            print("\n👋 Programm beendet. Auf Wiedersehen!")
            break
        else:
            print("\n❌ Ungültige Auswahl, bitte versuchen Sie es erneut.")
        
        input("\n[Enter] drücken, um zum Menü zurückzukehren...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Abbruch durch Benutzer.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Ein unerwarteter Fehler ist aufgetreten: {e}")
        traceback.print_exc()
        sys.exit(1)