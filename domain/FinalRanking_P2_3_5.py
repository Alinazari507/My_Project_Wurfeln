from dataclasses import dataclass
from typing import List, Dict, Union, Any
import re

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
            # Konvertiert PlayerScore-Objekte in ein Dictionary
            self.player_scores = {ps.name: ps.score for ps in player_scores}
    
    def get_final_ranking_with_ties(self) -> List[RankResult]:
        """
        Berechnet die Rangliste (Standard Competition Ranking: 1, 1, 3...).
        Dies ist die Logik-Basis für die Rich-Tabelle in der Application-Layer.
        """
        if not self.player_scores:
            return []

        # Sortierung nach Punkten absteigend (Akzeptanzkriterium 3)
        sorted_items = sorted(
            self.player_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        result = []
        previous_score = None
        current_rank = 0
        
        for index, (player, score) in enumerate(sorted_items):
            if score != previous_score:
                current_rank = index + 1
            
            result.append(RankResult(
                rank=current_rank,
                player_name=player,
                score=score
            ))
            previous_score = score
        
        return result
    
    def get_winner(self) -> List[str]:
        """Ermittelt alle Spieler auf dem ersten Platz."""
        if not self.player_scores:
            return []
        max_score = max(self.player_scores.values())
        return [name for name, score in self.player_scores.items() if score == max_score]

    # HINWEIS: format_final_ranking_table() und display_podium() wurden entfernt,
    # da die visuelle Darstellung nun über die Rich-Bibliothek in der 
    # Application-Layer erfolgt (Separation of Concerns).