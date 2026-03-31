import random

class GameRound:
    """
    Verwaltet die zentrale Spiellogik (Domain Layer).
    Zuständig für Rundenmanagement, Würfel-Logik und Punktestände.
    """
    
    def __init__(self, players, max_rounds):
        if not players:
            raise ValueError("❌ Fehler: Mindestens ein Spieler erforderlich!")
        if max_rounds < 1:
            raise ValueError("❌ Fehler: Rundenlimit muss mindestens 1 sein!")
        
        self.players = players
        self.max_rounds = max_rounds
        self.current_round = 1
        self.current_player_index = 0
        self.player_scores = {player: 0 for player in players}
        self.game_over = False
    
    def get_current_player(self):
        return self.players[self.current_player_index]
    
    def get_game_status(self):
        """ Gibt eine Momentaufnahme des aktuellen Spielstands zurück. """
        return {
            "round": self.current_round,
            "max_rounds": self.max_rounds,
            "current_player": self.get_current_player(),
            "current_player_number": self.current_player_index + 1,
            "total_players": len(self.players),
            "scores": self.player_scores.copy(),
            "game_over": self.game_over
        }
    
    def execute_player_turn(self):
        """ Führt einen Würfelwurf aus und aktualisiert den Spielzustand. """
        current_player = self.get_current_player()
        dice_result = random.randint(1, 6)
        
        # Score aktualisieren
        self.player_scores[current_player] += dice_result
        
        # Nächster Spieler (Modulo-Rechnung für den Kreis-Ablauf)
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        # Prüfung, ob eine vollständige Runde beendet wurde
        if self.current_player_index == 0:
            self.current_round += 1
            if self.current_round > self.max_rounds:
                self.game_over = True
        
        return {
            "player": current_player,
            "dice_result": dice_result,
            "total_score": self.player_scores[current_player]
        }

    def get_final_scores(self):
        """ Sortiert die Spieler nach Punkten (absteigend). """
        return sorted(self.player_scores.items(), key=lambda item: item[1], reverse=True)