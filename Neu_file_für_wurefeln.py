import random

def wuerfel_spiel():
    statistik = [0] * 6
    anzahl_wuerfe = 0

    print("=== WILLKOMMEN ZUM LIVE-WÜRFEL-DEMO ===")
    print("Steuerung: [Enter] = Würfeln | [s] = Statistik | [q] = Beenden")

    while True:
        eingabe = input("\nDeine Wahl: ").lower().strip()

        if eingabe == "q":
            print(f"Demo beendet. Wir haben insgesamt {anzahl_wuerfe} Mal gewürfelt.")
            break

        elif eingabe == "s":
            print(f"\n--- AKTUELLE STATISTIK ({anzahl_wuerfe} Würfe) ---")
            for zahl, menge in enumerate(statistik, start=1):
                balken = "*" * menge
                print(f"Zahl {zahl}: {menge:2}x | {balken}")
            print("------------------------------------------")

        elif eingabe == "":
            wurf = random.randint(1, 6)
            anzahl_wuerfe += 1
            statistik[wurf - 1] += 1
            print(f"🎲 Ergebnis: {wurf}  (Wurf Nr. {anzahl_wuerfe})")

            if anzahl_wuerfe == 50:
                print("\n🔥 Ziel erreicht! 50 Würfe voll.")
                for z, m in enumerate(statistik, start=1):
                    print(f"Zahl {z}: {m:2}x {'*' * m}")
                break

        else:
            print(f"⚠️ '{eingabe}' ist kein gültiger Befehl!")

if __name__ == "__main__":
    wuerfel_spiel()

