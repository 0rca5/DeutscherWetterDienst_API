import pymongo
from flask import request
from flask import Flask
from graphene import Schema
from Controller.Wetterdienst_Query import DWDQuery
from Service.Wetterdienst_Service import WetterdienstService
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

def run_app():
    app.run()


if __name__ == "__main__":
    #Service Instanz
    serv = WetterdienstService.instance()

    serv.create_new_geoindex("crowd_meldungen",[("location", pymongo.GEOSPHERE)])

    t = threading.Thread(target=run_app)
    t.start()

    while True:
        json_data = serv.get_json_data(
            "https://s3.eu-central-1.amazonaws.com/app-prod-static.warnwetter.de/v16/crowd_meldungen_overview_v2.json")
        serv.insert_json_data_into_db("crowd_meldungen", json_data, "meldungId")
        time.sleep(60)