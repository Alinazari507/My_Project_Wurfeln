from dataclasses import dataclass
from typing import List, Dict, Union, Any

@dataclass
class RankResult:
    """Repräsentiert ein einzelnes Ranking-Ergebnis."""
    rank: int
    player_name: str
    score: int

class FinalRanking:
    """
    Verwaltet die finale Rangliste mit intelligenter Gleichstand-Logik.
    Kriterium: Spieler mit gleicher Punktzahl erhalten den gleichen Rang.
    """
    
    def __init__(self, player_scores: Union[Dict[str, int], List[Any]]):
        """
        Initialisiert die Rangliste und normalisiert die Eingabedaten.
        """
        if isinstance(player_scores, dict):
            self.player_scores = player_scores.copy()
        else:
            # Konvertiert PlayerScore-Objekte oder ähnliche Strukturen in ein Dictionary
            self.player_scores = {ps.name: ps.score for ps in player_scores}
    
    def get_final_ranking_with_ties(self) -> List[RankResult]:
        """
        Berechnet die Rangliste unter Berücksichtigung von Gleichständen.
        Logik: 1, 1, 3, 4, 4, 6 (Standard Competition Ranking).
        """
        if not self.player_scores:
            return []

        # Sortierung nach Punkten absteigend
        sorted_items = sorted(
            self.player_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        result = []
        previous_score = None
        
        for index, (player, score) in enumerate(sorted_items):
            # Wenn der Score anders ist als der vorherige, wird der Rang auf (Index + 1) gesetzt
            if score != previous_score:
                current_rank = index + 1
            
            # Speicherung als RankResult Dataclass
            result.append(RankResult(
                rank=current_rank,
                player_name=player,
                score=score
            ))
            previous_score = score
        
        return result
    
    def get_winner(self) -> List[str]:
        """
        Ermittelt alle Spieler auf dem ersten Platz.
        """
        if not self.player_scores:
            return []
        
        max_score = max(self.player_scores.values())
        return [name for name, score in self.player_scores.items() if score == max_score]
    
    def get_podium(self) -> Dict[str, List[RankResult]]:
        """
        Gruppiert die Top 3 Platzierungen für die Siegerehrung.
        """
        ranking = self.get_final_ranking_with_ties()
        podium = {'gold': [], 'silver': [], 'bronze': []}
        
        for item in ranking:
            if item.rank == 1:
                podium['gold'].append(item)
            elif item.rank == 2:
                podium['silver'].append(item)
            elif item.rank == 3:
                podium['bronze'].append(item)
        
        return podium
    
    def format_final_ranking_table(self) -> str:
        """
        Erstellt eine formatierte Tabelle der Endergebnisse.
        """
        ranking = self.get_final_ranking_with_ties()
        lines = [
            "\n" + "=" * 55,
            "🏆 FINALE RANGLISTE - SIEGEREHRUNG 🏆".center(55),
            "=" * 55
        ]
        
        for item in ranking:
            # Medaillen-Zuweisung
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(item.rank, f"{item.rank:>2}.")
            line = f"{medal}  Platz {item.rank:<2} | {item.player_name:<20} | {item.score:>4} Punkte"
            lines.append(line)
        
        lines.append("=" * 55 + "\n")
        return "\n".join(lines)
    
    def display_podium(self):
        """
        Gibt das Podium grafisch in der Konsole aus.
        """
        podium = self.get_podium()
        print("\n" + "🎉" * 25)
        print("🏆 SIEGEREHRUNG - PODIUM 🏆".center(50))
        print("🎉" * 25)
        
        sections = [('gold', '🥇 GOLD'), ('silver', '🥈 SILBER'), ('bronze', '🥉 BRONZE')]
        
        for key, title in sections:
            if podium[key]:
                print(f"\n{title}:")
                for item in podium[key]:
                    print(f"   ⭐ {item.player_name} ({item.score} Punkte)")
        
        print("\n" + "🎉" * 25 + "\n")

# =================================================================
# EXECUTION (ENTRY POINT)
# =================================================================
if __name__ == "__main__":
    # Beispiel-Daten mit Gleichständen
    test_scores = {
        "Lukas": 50,
        "Hanna": 50,
        "Maximilian": 40,
        "Sarah": 30,
        "Tom": 30,
        "Mia": 10
    }
    
    ranking_service = FinalRanking(test_scores)
    
    # 1. Tabellarische Anzeige
    print(ranking_service.format_final_ranking_table())
    
    # 2. Podium Anzeige
    ranking_service.display_podium()
    
    # 3. Gewinner Liste
    print(f"Gewinner: {', '.join(ranking_service.get_winner())}")