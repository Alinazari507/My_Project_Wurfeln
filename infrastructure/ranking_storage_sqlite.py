import sqlite3
from domain.FinalRanking_P2_3_5 import RankResult

class SQLiteRankingStorage:
    def __init__(self, connection):
        """
        Initialisiert den Storage mit einer bestehenden SQLite-Verbindung.
        """
        self.connection = connection

    def create_schema(self):
        """
        Erstellt die notwendigen Tabellen für Rankings, Sessions und Einzelwürfe (P2.5.3).
        """
        # Tabelle für finale Spielergebnisse (P2.5.1)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS rankings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        """)
        
        # Tabelle für pausierte Spielsessions (P2.5.2)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_names TEXT NOT NULL,
                current_round INTEGER NOT NULL,
                max_rounds INTEGER NOT NULL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tabelle für die lückenlose Aufzeichnung aller Würfe (P2.5.3)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS dice_rolls (
                roll_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                player_name TEXT NOT NULL,
                dice_value INTEGER NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES game_sessions (session_id)
            )
        """)
        self.connection.commit()

    # --- Methoden für Rankings (P2.5.1) ---
    
    def save_result(self, result: RankResult):
        """Speichert ein finales RankResult-Objekt in der Datenbank."""
        query = "INSERT INTO rankings (player_name, score) VALUES (?, ?)"
        self.connection.execute(query, (result.player_name, result.score))
        self.connection.commit()

    def get_all(self):
        """Gibt alle gespeicherten Rankings für Validierungen zurück."""
        query = "SELECT player_name, score FROM rankings"
        cursor = self.connection.execute(query)
        rows = cursor.fetchall()
        return [RankResult(rank=0, player_name=row[0], score=row[1]) for row in rows]

    # --- Methoden für Lobby & Sessions (P2.5.2) ---

    def save_session(self, player_names: str, current_round: int, max_rounds: int) -> int:
        """
        Speichert oder aktualisiert den Status einer Spielsession.
        Gibt die session_id des neuen Eintrags zurück.
        """
        query = """
            INSERT INTO game_sessions (player_names, current_round, max_rounds)
            VALUES (?, ?, ?)
        """
        cursor = self.connection.execute(query, (player_names, current_round, max_rounds))
        self.connection.commit()
        return cursor.lastrowid

    def get_active_sessions(self):
        """Ruft alle pausierten Spielstände für die Lobby ab."""
        query = """
            SELECT session_id, player_names, current_round, max_rounds, last_updated 
            FROM game_sessions
            ORDER BY last_updated DESC
        """
        cursor = self.connection.execute(query)
        return cursor.fetchall()

    def get_session_by_id(self, session_id: int):
        """Sucht eine spezifische Session anhand der ID."""
        query = "SELECT player_names, current_round, max_rounds FROM game_sessions WHERE session_id = ?"
        cursor = self.connection.execute(query, (session_id,))
        return cursor.fetchone()

    # --- Methoden für Einzelwürfe (P2.5.3) ---

    def save_roll(self, session_id: int, player_name: str, value: int):
        """
        Sichert jeden einzelnen Wurf unmittelbar in der Datenbank.
        Garantiert Datenintegrität auch bei plötzlichem Programmabbruch.
        """
        query = "INSERT INTO dice_rolls (session_id, player_name, dice_value) VALUES (?, ?, ?)"
        self.connection.execute(query, (session_id, player_name, value))
        self.connection.commit()

    def get_rolls_for_session(self, session_id: int):
        """Ruft alle Würfe einer Session ab, um den Spielstand zu rekonstruieren."""
        query = "SELECT player_name, dice_value FROM dice_rolls WHERE session_id = ? ORDER BY timestamp ASC"
        cursor = self.connection.execute(query, (session_id,))
        return cursor.fetchall()