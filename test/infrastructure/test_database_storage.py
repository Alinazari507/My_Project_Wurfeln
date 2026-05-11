import unittest
import sqlite3
from assertpy import assert_that
from infrastructure.ranking_storage_sqlite import SQLiteRankingStorage
from domain.FinalRanking_P2_3_5 import RankResult

class TestDatabaseStorage(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.storage = SQLiteRankingStorage(self.connection)
        self.storage.create_schema()

    def test_should_save_and_retrieve_rank_result(self):
        # GIVEN
        result = RankResult(rank=1, player_name="Max Mustermann", score=100)
        
        # WHEN
        self.storage.save_result(result)
        all_results = self.storage.get_all()
        
        # THEN
        # Wir prüfen zuerst mit Standard-Unittest
        self.assertEqual(len(all_results), 1)
        
        # Und dann mit assertpy (is_length statt has_size zur Sicherheit)
        assert_that(all_results).is_type_of(list).is_length(1)
        assert_that(all_results[0].player_name).is_equal_to("Max Mustermann")

    def tearDown(self):
        self.connection.close()
    def test_should_handle_database_error_gracefully(self):
        # GIVEN: Wir schließen die Verbindung, um einen Fehler zu provozieren
        self.connection.close()
        result = RankResult(rank=1, player_name="Error Test", score=0)
        
        # WHEN / THEN: Es sollte kein fataler Absturz passieren, 
        # oder wir prüfen, ob eine Exception gefangen wird
        try:
            self.storage.save_result(result)
        except Exception as e:
            assert_that(str(e)).contains("closed")
    def test_should_save_and_list_sessions_in_lobby(self):
        # GIVEN: Ein pausiertes Spiel mit 2 Spielern
        self.storage.save_session("Lukas, Hanna", 2, 5)
        
        # WHEN: Die Lobby die aktiven Sessions abruft
        sessions = self.storage.get_active_sessions()
        
        # THEN: Wir erwarten, dass das Spiel in der Liste auftaucht
        assert_that(sessions).is_length(1)
        assert_that(sessions[0][1]).is_equal_to("Lukas, Hanna")
        assert_that(sessions[0][2]).is_equal_to(2) # current_round