from graphene import ObjectType, Argument, String, ID, Field, List
from Controller.Model import MeldungType, LocationType
from Service.Wetterdienst_Service import WetterdienstService


class DWDQuery(ObjectType):
    """Eine Klasse die Anfragen an die wetterdienst-Datenbank bearbeitet"""

    warnungen = Field(List(MeldungType),
                      meldungId = Argument(ID,required = False),
                      place=Argument(String, required=False),
                      lon=Argument(String, required=False),
                      lat=Argument(String, required=False),
                      category=Argument(String, required=False),
                      auspraegung=Argument(String, required=False),
                      location=Argument(LocationType, required=False))

    lokaleWarnungen = Field(List(MeldungType),
                             lon = Argument(String,required = True),
                             lat = Argument(String, required = True))

    hoehendaten = Field(List(MeldungType),
                       meldungId=Argument(ID, required=False),
                       place=Argument(String, required=False),
                       lon=Argument(String, required=False),
                       lat=Argument(String, required=False),
                       category=Argument(String, required=False),
                       auspraegung=Argument(String, required=False),
                       location=Argument(LocationType, required=False))

    def resolve_warnungen(root, info, meldungId = None, place=None, lon=None, lat=None, category=None, auspraegung=None, location=None):
        """
        hilft, Abfragen zu beantworten, indem Daten für das Feld warnungen abgerufen werden.

        :param info:
        :param meldungId (ID): ID der Meldung
        :param place (String): Ort der Meldung
        :param lon (String): Längengrad der Meldung
        :param lat (String): Breitengrad der Meldung
        :param category (String): Art des Wetters
        :param auspraegung (String): Ausprägung des Wetters
        :param location (LocationType): enthält Längen- und Breitengrad als Koordinatenpunkt
        :return: Liste an documents
        """
        serv = WetterdienstService.instance()

        query = {}
        if meldungId:
           query["meldungId"] = meldungId
        if place:
            query["place"] = place
        if lon:
            query["lon"] = lon
        if lat:
            query["lat"] = lat
        if category:
            query["category"] = category
        if auspraegung:
            query["auspraegung"] = auspraegung
        if location:
            query["location"] = location

        meldungs_result = serv.find_warning("crowd_meldungen", query)
        meldungsliste = list(meldungs_result)

        return meldungsliste

    def resolve_lokaleWarnungen(root, info, lon = None, lat = None):
        """
        hilft, Abfragen zu beantworten, indem Daten für das Feld lokaleWarnungen abgerufen werden

        :param info:
        :param lon: Längengrad
        :param lat: Breitengrad
        :return: Liste an documents
        """

        serv = WetterdienstService.instance()

        lokale_meldungen = serv.find_nearest_warning("crowd_meldungen",float(lon),float(lat))

        meldungsliste = list(lokale_meldungen)

        return meldungsliste

    def resolve_hoehendaten(root, info,meldungId = None, place=None, lon=None, lat=None, category=None, auspraegung=None, location = None):
        serv = WetterdienstService.instance()

        query = {}
        if meldungId:
            query["meldungId"] = meldungId
        if place:
            query["place"] = place
        if lon:
            query["lon"] = lon
        if lat:
            query["lat"] = lat
        if category:
            query["category"] = category
        if auspraegung:
            query["auspraegung"] = auspraegung
        if location:
            query["location"] = location

        meldungs_result = serv.find_warning("crowd_meldungen", query)
        meldungsliste = list(meldungs_result)

        return meldungsliste