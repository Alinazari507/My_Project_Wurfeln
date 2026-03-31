"""
P2.3.4 - GameState Manager
Verwaltet den aktuellen Spielstand mit Rundeninfo und aktueller Spielerin
"""

from dataclasses import dataclass, asdict
from typing import List, Optional
from datetime import datetime


@dataclass
class PlayerScore:
    """Spieler mit Punktestand"""
    name: str
    score: int


@dataclass
class GameState:
    """Aktueller Spielstand mit Runde und aktuellem Spieler"""
    current_round: int
    current_player_name: str
    player_scores: List[PlayerScore]
    timestamp: str
    
    def __post_init__(self):
        """Zeitstempel wird beim Erstellen gesetzt"""
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """Konvertiert GameState zu Dictionary"""
        return {
            "current_round": self.current_round,
            "current_player_name": self.current_player_name,
            "player_scores": [asdict(ps) for ps in self.player_scores],
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GameState':
        """Erstellt GameState aus Dictionary"""
        player_scores = [
            PlayerScore(name=ps['name'], score=ps['score'])
            for ps in data.get('player_scores', [])
        ]
        return cls(
            current_round=data['current_round'],
            current_player_name=data['current_player_name'],
            player_scores=player_scores,
            timestamp=data.get('timestamp', '')
        )
