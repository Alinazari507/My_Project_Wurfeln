# Importieren von Bibliotheken
import os
import random
import json

# Dateiname für die Speicherung
datei_name = "spiel_statistik.json"

# Funktion zum Speichern der Statistik
def statistik_speichern(statistik):
    with open(datei_name, "w") as f:
        json.dump(statistik, f)
    print(f"Spielstand gespeichert!")

# Funktion zum Laden der Statistik
def statistik_laden():
    if os.path.exists(datei_name):
        with open(datei_name, "r") as f:
            return json.load(f)
    return [0, 0, 0, 0, 0, 0]

# Hauptfunktion des Spiels
def wuerfel_spiel():
    # Geladene Daten prüfen
    geladene_daten = statistik_laden()
    statistik = [0, 0, 0, 0, 0, 0]

    if sum(geladene_daten) > 0:
        print("\n---Gespeicherter Spielstand gefunden---")
        print(f"Bisherige Würfe: {sum(geladene_daten)}")
        entscheidung = input("Möchtest du den alten Spielstand laden? (j/n): ").lower().strip()
        if entscheidung == "j":
            statistik = geladene_daten
            print("Spielstand wurde geladen. Viel Spaß!")
        else:
            print("Neues Spiel wird gestartet!")

    gesamtzahl_wuerfe = sum(statistik)

    # Endlosschleife für das Würfeln
    while True:
        wuerfeln = random.randint(1, 6)
        gesamtzahl_wuerfe += 1
        statistik[wuerfeln - 1] += 1

        print(f"Du hast eine {wuerfeln} gewürfelt!")

        # Limit 50 Würfe
        if sum(statistik) == 50:
            print("\n-------------------")
            print("50 Würfe erreicht! Das Spiel ist hier beendet.")
            print(f"Hier ist die Gesamtzahl der Würfe: {sum(statistik)}")
            print("---- Deine Abschluss-Statistik ----")
            for zahl, anzahl in enumerate(statistik, start=1):
                print(f"Würfel {zahl}: {anzahl} mal")
            print("-------------------------\n")
            break

        # Abfrage vom Spieler
        frage_spieler = input("Nochmal Würfeln (j), Spiel Beenden und Speichern (q), Statistik anzeigen (s): ").lower().strip()

        if frage_spieler == "q":
            statistik_speichern(statistik)
            print("Vielen Dank fürs Spielen. Dein Spielstand wurde gespeichert.")
            break
        elif frage_spieler == "s":
            print(f"\n---Deine Statistik---")
            print(f"Hier ist die Gesamtzahl der Würfe: {sum(statistik)}")
            print("--------------------")
            for zahl, anzahl in enumerate(statistik, start=1):
                print(f"Zahl {zahl}: {anzahl:2} mal Gewürfelt")
            print("-------------------\n")
            break
        else:
            print(f"Nächster Wurf")

# Spiel starten
if __name__ == "__main__":
    wuerfel_spiel()

