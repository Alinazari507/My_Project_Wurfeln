"""
P2.3.4 - Extended Game Storage Manager
Verwaltet manuelles und automatisches Speichern/Laden mit Rundeninfo
"""

import json
import os
from pathlib import Path
from typing import Optional, Callable
from datetime import datetime
from domain.GameState_P2_3_4 import GameState


class ExtendedGameStorage:
    """Speichert und lädt Spielstände mit Runden und aktuellem Spieler"""
    
    def __init__(self, storage_path: str = "archive"):
        """
        Initialisiert den Speicher-Manager
        
        Args:
            storage_path: Verzeichnis für Speicherdateien
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.auto_save_callback: Optional[Callable] = None
    
    def manual_save(self, game_state: GameState) -> str:
        """
        Speichert Spielstand manuell
        
        Args:
            game_state: Aktueller Spielstand
            
        Returns:
            Pfad zur gespeicherten Datei
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"save_manual_{timestamp}.json"
        filepath = self.storage_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(game_state.to_dict(), f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def auto_save(self, game_state: GameState) -> str:
        """
        Speichert Spielstand automatisch nach Runde
        
        Args:
            game_state: Aktueller Spielstand
            
        Returns:
            Pfad zur gespeicherten Datei
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"save_auto_round{game_state.current_round}_{timestamp}.json"
        filepath = self.storage_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(game_state.to_dict(), f, indent=2, ensure_ascii=False)
        
        # Callback für Benachrichtigung
        if self.auto_save_callback:
            self.auto_save_callback(filename, game_state.current_round)
        
        return str(filepath)
    
    def load_game(self, filepath: str) -> Optional[GameState]:
        """
        Lädt Spielstand aus Datei
        
        Args:
            filepath: Pfad zur Speicherdatei
            
        Returns:
            GameState oder None wenn Datei nicht existiert
        """
        path = Path(filepath)
        
        if not path.exists():
            print(f"⚠️ Datei nicht gefunden: {filepath}")
            return None
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return GameState.from_dict(data)
        except Exception as e:
            print(f"❌ Fehler beim Laden: {e}")
            return None
    
    def list_saves(self) -> list:
        """
        Listet alle gespeicherten Spiele auf
        
        Returns:
            Liste von Dateinamen
        """
        if not self.storage_path.exists():
            return []
        
        saves = sorted(
            [f.name for f in self.storage_path.glob("save_*.json")],
            reverse=True
        )
        return saves
    
    def set_auto_save_callback(self, callback: Callable) -> None:
        """
        Setzt Callback für automatische Speicher-Benachrichtigungen
        
        Args:
            callback: Funktion(filename, round_number)
        """
        self.auto_save_callback = callback
