import pymongo
import requests
import json
from pymongo.errors import OperationFailure
from Persistence.Wetterdienst_Persistence import WetterdienstPersistence

class WetterdienstService():

    """Eine Klasse die einen Wetterdienst-Service repräsentiert

    Methoden:
    instance()
    find_nearest_warning()
    find_warning()
    get_json_data()
    insert_json_into_db()
    create_index()
    update_one()
    create_new_geo_index()
    """

    _instance = None
    _persistence = None

    def __init__(self):
        raise RuntimeError("Nutze stattdessen instance()-Methode")

    @classmethod
    def instance(cls):
        """
        Sorgt dafür, dass immer die gleiche WetterdienstService-Instanz referenziert wird
        und initialisert eine WetterdienstPersistence-Instanz für alle Methoden.

        :return: Eine WetterdienstService-Instanz
        """
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._persistence = WetterdienstPersistence()
        return cls._instance

    def find_nearest_warning(cls, collection_name, lon, lat, limit = 3):
        """
        Gibt eine limitierte Liste an documents aus einer collection aus,
        die sich in der Nähe des übergebenen Längen- und Breitengrad befinden.

        :param collection_name: (String) Name der collection
        :param lon: (Int, Float oder String) Längengrad
        :param lat: (Int, Float oder String) Breitengrad
        :param limit: (Int) Maximale Anzahl der documents in der Liste
        :return: list
        """
        return cls._persistence.find_documents(collection_name,
            {"location": {"$near": {"$geometry": {"type": "Point", "coordinates": [float(lon), float(lat)]}}}}
            )[:limit]

    def find_warning(cls, collection_name, query):
        """
        Gibt eine Liste an documents aus einer collection aus, die der Anfrage entsprechen.

        :param collection_name: (String) Name der collection
        :param query: (dict) Anfrage an die collection
        :return: list
        """
        return cls._persistence.find_documents(collection_name, query)

    def get_json_data(self, url, field_specifier = None):
        """
        Gibt ein JSON (dict) zurück, indem es die als Argument übergebene URL anfragt.

        :param url: (String) URL an die eine GET-Anfrage gesendet wird
        :return: dict
        """
        response = requests.get(url)
        data = json.loads(response.content)

        if field_specifier:
            return data[field_specifier]
        else:
            return data

    def insert_json_data_into_db(cls, collection_name, json_data, dup_field, index_specifier = pymongo.ASCENDING):
        """
        Fügt eine Liste an dictionaries/JSON-Objekten einer collection hinzu und verhindert die Duplikation von documents.

        :param collection_name: (String) Name der collection
        :param json_data: (list) Liste an dictionaries/JSON
        :param dup_field: (String) Feld, dass zum Index deklariert werden soll, um Duplikation zu verhindern.
        :param index_specifier: (pymongo collection level utility) Spezifiziert die Anordnung des Indexes oder die Art des Indexes. Standard: aufsteigend (pymongo.ASCENDING)
        :return: None
        """
        #dedupe_key -> ID um Duplikate zu vermeiden
        cls._persistence.create_index(collection_name, [(dup_field, index_specifier)])
        try:
            cls._persistence.insert_many(collection_name, json_data)
        except:
            print(f"Daten wurden in {collection_name} geschrieben. Duplikate wurden anhand {dup_field}-Index verhindert.")

        return

    def create_index(cls, collection_name, index_field, index_specifier = pymongo.ASCENDING):
        """
        Setzt ein bestimmtes Feld in einer collection als Index.

        :param collection_name: (String) Name der collection
        :param index_field: (String) Name des Feldes
        :param index_specifier: (pymongo collection level utility) Spezifiziert die Anordnung des Indexes oder die Art des Indexes. Standard: aufsteigend (pymongo.ASCENDING)
        :return: None
        """

        cls._persistence.create_index(collection_name, [(index_field, index_specifier)])
        return

    def update_one(cls, collection_name, document, query):
        """
        Passt ein document in einer collection nach den Anforderungen in der Anfrage an.

        :param collection_name: (String) Name der collection
        :param document: (dict) Das anzupassende document
        :param query: (dict) Anfrage, die die Anpassungen enthält
        :return: None
        """
        cls._persistence.update_one(collection_name, document, query)
        return

    def insert_document(cls, collection_name, document):
        """

        :param collection_name: (String) Name der collection
        :param document: Zu erstellendes document in der Form {"feld_name" : Wert, "feld_name2": Wert2}
        :return:
        """
        cls._persistence.insert_document(collection_name, document)
        return

    def create_new_geoindex(cls, collection_name, geo_field_name="location", index_specifier=pymongo.GEOSPHERE):

        """
        Setzt ein location-Feld in einer collection als GEO-Index.

        :param collection_name: (String) Name der Collection
        :param geo_field_name:(String) Name des Feldes, das als GEO-Index deklariert werden soll. Standard: "location"
        :param index_specifier: (pymongo collection level utility) Art des GEO-Index. Standard: pymongo.GEOSPHERE
        :return: None
        """

        query = {geo_field_name: {"$exists": False}}

        if cls._persistence.find_documents(collection_name, query):

            for x in cls._persistence.find_documents(collection_name, query):
                lon = x["lon"]
                lat = x["lat"]
                cls.update_one(collection_name, x, {"$set": {geo_field_name: {"lon": float(lon), "lat": float(lat) }}})

        #try:
    #        cls._persistence.create_index(collection_name, [(geo_field_name, index_specifier)])
#
 #       except OperationFailure:
  #          print("Diesen GEO-Index gibt es bereits")

        return