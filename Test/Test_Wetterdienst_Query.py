import unittest
import pymongo
import responses
from unittest.mock import patch
from Controller.Wetterdienst_Query import DWDQuery


class TestDWDQuery(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Legt die Konfigurationen (z.B Instanzen oder Variablen die bei jedem Test benötigt werden) vor einem Testdurchlauf fest"""
        cls.dwd = DWDQuery()

    @classmethod
    def tearDownClass(cls):
        """Legt die Konfigurationen nach einem Testdurchlauf fest"""
        pass
    @patch('Service.Wetterdienst_Service.WetterdienstService.find_warning')
    def test_resolve_warnungen(self,mock_find_warnings):
       self.dwd.resolve_warnungen("info", place = "München", category ="BLITZE")

       mock_find_warnings.assert_called_with("crowd_meldungen", {"place": "München", "category": "BLITZE"})

    @patch('Service.Wetterdienst_Service.WetterdienstService.find_nearest_warning')
    def test_resolve_lokaleWarnungen(self,mock_find_nearest_warnings):
       self.dwd.resolve_lokaleWarnungen("info", lon = "77", lat ="90")

       mock_find_nearest_warnings.assert_called_with("crowd_meldungen", 77, 90)


if __name__ == "__main__":
    unittest.main()