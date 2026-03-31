"""
P2.3.3: Rangliste nach jeder Runde - DOMAIN LAYER

Verantwortung: Ranking-Logik und Geschäftsregeln
- Ranglisten-Berechnung
- Sortierung nach Punkten (absteigend - umgekehrter Bubble Sort)
- Rang-Bestimmung
"""


class Ranking:
    """
    Verwaltet die Rangliste der Spieler*innen.
    Sortiert Spieler*innen nach Punkten (absteigend).
    
    Akzeptanzkriterium:
    - Nach jeder Runde wird die Rangliste nach Punkten absteigend angezeigt
    - Implementierung: Umgekehrter Bubble Sort
    """
    
    def __init__(self, player_scores):
        """
        Initialisiert die Rangliste mit Spieler-Scores.
        
        Args:
            player_scores (dict): {Spieler: Score, ...}
        """
        self.player_scores = player_scores.copy()
    
    @staticmethod
    def bubble_sort_descending(scores_dict):
        """
        Sortiert Spieler*innen nach Punkten (absteigend) mit Bubble Sort.
        
        Umgekehrter Bubble Sort:
        - Größere Werte "bubeln" nach oben
        - Ergebnis: Höchste Punkte zuerst
        
        Args:
            scores_dict (dict): {Spieler: Score, ...}
            
        Returns:
            list: Sortierte Liste [(Spieler, Score), ...]
        """
        # Konvertiere zu Liste
        items = list(scores_dict.items())
        n = len(items)
        
        # Bubble Sort (absteigend)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                # Vergleich: wenn links kleiner als rechts, tausche (absteigend)
                if items[j][1] < items[j + 1][1]:
                    items[j], items[j + 1] = items[j + 1], items[j]
                    swapped = True
            
            # Optimierung: Abbruch wenn keine Tausch stattgefunden
            if not swapped:
                break
        
        return items
    
    def get_ranking(self):
        """
        Gibt die aktuelle Rangliste (sortiert absteigend nach Punkten) zurück.
        
        Returns:
            list: [(Spieler, Score), ...] - sortiert absteigend
        """
        return self.bubble_sort_descending(self.player_scores)
    
    def get_ranking_with_rank(self):
        """
        Gibt die Rangliste mit Rangplätzen zurück.
        
        Returns:
            list: [(Rang, Spieler, Score), ...] - mit Platzierung
        """
        ranking = self.get_ranking()
        return [(rank + 1, player, score) for rank, (player, score) in enumerate(ranking)]
    
    def get_player_rank(self, player):
        """
        Gibt den aktuellen Rang eines bestimmten Spielers zurück.
        
        Args:
            player (str): Name des Spielers
            
        Returns:
            int: Rang (1 = erster Platz)
        """
        ranking = self.get_ranking()
        for rank, (p, score) in enumerate(ranking, 1):
            if p == player:
                return rank
        return -1  # Spieler nicht gefunden
    
    def update_scores(self, player_scores):
        """
        Aktualisiert die Scores und neu sortiert.
        
        Args:
            player_scores (dict): {Spieler: Score, ...}
        """
        self.player_scores = player_scores.copy()
    
    def get_top_3(self):
        """
        Gibt die Top 3 Spieler*innen zurück.
        
        Returns:
            list: [(Spieler, Score), ...] - max. 3 Einträge
        """
        ranking = self.get_ranking()
        return ranking[:3]
    
    def get_leader(self):
        """
        Gibt den aktuellen Führenden zurück.
        
        Returns:
            tuple: (Spieler, Score) oder (None, 0) falls leer
        """
        ranking = self.get_ranking()
        return ranking[0] if ranking else (None, 0)
