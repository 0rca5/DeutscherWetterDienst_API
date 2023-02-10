import pymongo
from flask import request, jsonify
from flask import Flask
from graphene import Schema
from graphqlAPI.modules.Wetterdienst_Query import DWDQuery
from graphqlAPI.modules.Wetterdienst_Service import WetterdienstService
import time
import threading

app = Flask(__name__)

@app.route("/graphql")
def request_query():
    query_string = str(request.get_json()["query"])
    schema = Schema(query=DWDQuery)
    result = schema.execute(query_string)
    field_key = list(result.data.keys())[0]
    return result.data[field_key]

@app.route("/heightInfo")
def request_height():
    query_string = str(request.get_json()["query"])
    geo_data_list =[]
    schema = Schema(query=DWDQuery)
    result = schema.execute(query_string)
    print(result)
    requested_document_list = result.data[list(result.data.keys())[0]]
    print(requested_document_list[0])

    for document in requested_document_list[:2]:
       location_field = document.get("location", {})
       geo_data_document = serv.find_warning("geo_daten", {"location": location_field})
       if geo_data_document:
           geo_data_list.append(geo_data_document[0].get("height", 0))
       else:
           height = serv.get_json_data(
             f"https://de-de.topographic-map.com/?_path=api.maps.getElevation&latitude={location_field['lat']}&longitude={location_field['lon']}&version=202302041229")
           serv.insert_json_data_into_db("geo_daten", {"height": height, "location": location_field},"location",pymongo.GEOSPHERE)
           geo_data_list.append(height)
    return jsonify({"heights": geo_data_list})


def run_app():
    app.run()


if __name__ == "__main__":
    #Service Instanz
    serv = WetterdienstService.instance()

    serv.create_new_geofield("crowd_meldungen", "location", pymongo.GEOSPHERE)
    serv.create_new_geofield("geo_daten", "location", pymongo.GEOSPHERE)

    t = threading.Thread(target=run_app)
    t.start()

    #Abfragen der DWD-API und einfügen in die collection in einem bestimten Zeitintervall
    while True:
        json_data = serv.get_json_data(
            "https://s3.eu-central-1.amazonaws.com/app-prod-static.warnwetter.de/v16/crowd_meldungen_overview_v2.json",field_specifier = "meldungen")
        serv.insert_json_data_into_db("crowd_meldungen", json_data, "meldungId")
        time.sleep(300)