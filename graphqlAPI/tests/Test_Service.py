import unittest
import pymongo
import responses
from unittest.mock import patch
from graphqlAPI.modules.Service import WetterdienstService


class TestWetterdienstService(unittest.TestCase):
    """
    Eine Klasse die den Wetterdienst-Service testet.

    Methoden:
    setUpClass()
    tearDownClass()
    test_get_json_data_returns_json()
    test_find_nearest_warning_calls_find_documents()
    test_find_nearest_warning_returns_limited_list()
    test_find_warning_calls_find_documents()
    test_insert_json_data_into_db_calls_create_index()
    test_insert_json_data_into_db_calls_insert_many()
    test_update_one_calls_update_one_from_persistence()
    test_create_index_calls_create_index_from_persistence()
    test_create_index_calls_create_index_from_persistence()
    test_create_new_geo_index_calls_find_documents_from_persistence()
    test_create_new_geo_index_calls_create_index_from_persistence()

    """

    serv = None

    @classmethod
    def setUpClass(cls):
        """Legt die Konfigurationen (z.B Instanzen oder Variablen die bei jedem Test benötigt werden) vor einem Testdurchlauf fest"""
        cls.serv = WetterdienstService.instance()

    @classmethod
    def tearDownClass(cls):
        """Legt die Konfigurationen nach einem Testdurchlauf fest"""
        pass

    @responses.activate
    def test_get_json_data_returns_json(self):
        """
        Testet, ob die get_json_data() ein JSON-Objekt zurückgibt.
        Wirft einen AssertionError, wenn der Test nicht bestanden ist.

        """
        responses.get(url = "http://url.com",
                      json = {"key":"value"},
                      status = 200)

        self.assertEqual(WetterdienstService.instance().get_json_data("http://url.com"), {"key":"value"})

    @patch('Persistence.Wetterdienst_Persistence.WetterdienstPersistence.find_documents')
    def test_find_nearest_warning_calls_find_documents(self,mock_find_documents):
        """
        Testet, ob die find_nearest_warning() die find_documents() aufruft.
        Wirft einen AssertionError, wenn der Test nicht bestanden ist.

        :param mock_find_documents: Mockt die find_documents
        """
        lon = 105
        lat = 93
        self.serv.find_nearest_warning("collection", lon, lat)
        mock_find_documents.assert_called_with("collection",
                        {"location": {"$near": {"$geometry": {"type": "Point", "coordinates": [float(lon), float(lat)]}}}}
                        )

    @patch('Persistence.Wetterdienst_Persistence.WetterdienstPersistence.find_documents')
    def test_find_nearest_warning_returns_limited_list(self, mock_find_documents):
        """
        Testet, ob die find_nearest_warning() eine dem Argument entsprechende limitierte Liste ausgibt.
        Wirft einen AssertionError, wenn der Test nicht bestanden ist.

        :param mock_find_documents: Mockt die find_documents() der WetterdienstPersistence-Klasse
        """
        lon = 105
        lat = 93
        limit = 2
        mock_find_documents.return_value = ["element1","element2","element3","element4","element5"]
        self.assertEqual(len(self.serv.find_nearest_warning("collection", lon, lat, limit)),limit)

    @patch('Persistence.Wetterdienst_Persistence.WetterdienstPersistence.find_documents')
    def test_find_warning_calls_find_documents(self, mock_find_documents):
        """
        Testet, ob die find_warning_calls() die find_documents() der WetterdienstPersistence-Klasse aufruft.
        Wirft einen AssertionError, wenn der Test nicht bestanden ist.

        :param mock_find_documents: Mockt die find_documents() der WetterdienstPersistence-Klasse
        """
        self.serv.find_warning("collection",{ "field_name": "field_value"})
        mock_find_documents.assert_called_with("collection", {"field_name": "field_value"})

    @patch('Persistence.Wetterdienst_Persistence.WetterdienstPersistence.create_index')
    def test_insert_json_data_into_db_calls_create_index(self, mock_create_index):
        """
        Testet, ob die insert_json_data_into_db() die create_index() der WetterdienstPersistence-Klasse aufruft.
        Wirft einen AssertionError, wenn der Test nicht bestanden ist.

        :param mock_create_index: Mockt die create_index() der WetterdienstPersistence-Klasse
        """
        collection_name = 'test_collection'
        json_data = [{'id': 1, 'name': 'test1'}, {'id': 2, 'name': 'test2'}]
        dedupe_key = 'id'

        self.serv.insert_json_data_into_db(collection_name, json_data, dedupe_key)
        mock_create_index.assert_called_with(collection_name,[(dedupe_key, pymongo.ASCENDING)])

    @patch('Persistence.Wetterdienst_Persistence.WetterdienstPersistence.insert_many')
    def test_insert_json_data_into_db_calls_insert_many(self, mock_insert_many):
        """
        Testet, ob die insert_json_data_into_db() die insert_many() der WetterdienstPersistence-Klasse aufruft.
        Wirft einen AssertionError, wenn der Test nicht bestanden ist.

        :param mock_insert_many: Mockt die insert_many() der WetterdienstPersistence-Klasse
        """
        collection_name = 'test2_collection'
        json_data = [{'id': 1, 'name': 'test1'}, {'id': 2, 'name': 'test2'}]
        dedupe_key = 'id'

        self.serv.insert_json_data_into_db(collection_name, json_data, dedupe_key)
        mock_insert_many.assert_called_with(collection_name, json_data)

    @patch('Persistence.Wetterdienst_Persistence.WetterdienstPersistence.update_one')
    def test_update_one_calls_update_one_from_persistence(self, mock_update_one):
        """
        Testet, ob die update_one() die update_one() der WetterdienstPersistence-Klasse aufruft.
        Wirft einen AssertionError, wenn der Test nicht bestanden ist.

        :param mock_update_one: Mockt die update_one() der WetterdienstPersistence-Klasse
        """
        collection_name = "collection"
        document = "document"
        query = {"key": "value"}

        self.serv.update_one(collection_name, document, query)
        mock_update_one.assert_called_with(collection_name, document, query)

    @patch('Persistence.Wetterdienst_Persistence.WetterdienstPersistence.create_index')
    def test_create_index_calls_create_index_from_persistence(self,mock_create_index):
        """
        Testet, ob die create_index() die create_index() der WetterdienstPersistence-Klasse aufruft.
        Wirft einen AssertionError, wenn der Test nicht bestanden ist.

        :param mock_create_index: Mockt die create_index() der WetterdienstPersistence-Klasse
        """
        collection_name = "collection"
        geo_field_name = "field_name"
        index_specifier = pymongo.ASCENDING

        self.serv.create_index(collection_name, geo_field_name, index_specifier)
        mock_create_index.assert_called_with(collection_name, [(geo_field_name, index_specifier)])

    @patch('Persistence.Wetterdienst_Persistence.WetterdienstPersistence.find_documents')
    def test_create_new_geo_field_calls_find_documents_from_persistence(self,mock_find_documents):
        """
        Testet, ob die create_new_geo_index() die find_documents() der WetterdienstPersistence-Klasse aufruft.
        Wirft einen AssertionError, wenn der Test nicht bestanden ist.

        :param mock_find_documents: Mockt die find_documents() der WetterdienstPersistence-Klasse
        """
        collection_name = "collection"
        geo_field_name = "field_name"
        index_specifier = pymongo.ASCENDING
        query = {geo_field_name: {"$exists": bool()}}

        self.serv.create_new_geoindex(collection_name, geo_field_name, index_specifier)
        mock_find_documents.assert_called_with(collection_name, query)




if __name__ == "__main__":
    unittest.main()