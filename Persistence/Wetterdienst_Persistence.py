import pymongo
from pymongo import MongoClient


class WetterdienstPersistence():
    """ Eine Klasse die eine Wetterdienst-Persistenz repräsentiert.

        Methoden:
        find_documents() -> list()
        delete_documents()
        create_index()
        update_one()
        insert_many()

    """
    def __init__(self):
        self.db = MongoClient("mongodb://localhost:27017")["wetterdienste"]

    def find_documents(self, collection_name, query):
        """
        Gibt eine Liste an documents einer collection aus, die den Anforderungen einer Anfrage entsprechen.

        :param collection_name: (String) Name der betroffenen collection, aus der die Liste an documents ausgegeben werden soll
        :param query: (dict) Anfrage an die collection
        :return: list()
        """
        return list(self.db[collection_name].find(query))

    def delete_documents(self, collection_name, query):
        """
        Löscht eine Menge an documents aus einer collection, die den Anforderungen einer Anfrage entsprechen.

        :param collection_name: (String) Name der collection, aus der die documents gelöscht werden sollen
        :param query: (dict) Anfrage an die collection
        :return: None
        """
        if self.db[collection_name].delete_many(query) == 0:
            raise Exception("Es konnten keine Dokumente gelöscht werden")

    def create_index(self, collection_name, index_list):
        """
        Setzt ein bestimmtes Feld in einer collection als Index.

        :param collection_name: (String) Name der collection
        :param index_list: (List) Liste von Tupeln in der Form (Index-Feld-Name, Index-Specifier)
        :return: None
        """
        self.db[collection_name].create_index(index_list, unique=True, background=True)
        return

    def update_one(self, collection_name, document, query):
        """
        Passt ein document in einer collection nach den Anforderungen in der Anfrage an.

        :param collection_name (String): Name der collection
        :param document (dict): Das anzupassende document
        :param query: Anfrage, die die Anpassungen enthält.
        :return: None
        """
        self.db[collection_name].update_one(document,query)
        return

    def insert_many(self, collection_name, document_list):
        """
        Fügt eine Liste an documents einer collection hinzu.

        :param collection_name: (String) Name der collection
        :param document_list: (list) Liste der documents die hinzuzufügen sind
        :return: None
        """
        self.db[collection_name].insert_many(document_list, ordered=False)
        return




