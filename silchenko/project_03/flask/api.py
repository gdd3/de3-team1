import requests
import json
import time
import datetime
from flask import Flask, abort, jsonify


app = Flask(__name__)
app.config["POSTGREST_API_URL"] = "http://localhost:3000/rpc/"


@app.route("/")
def hello():
    return "Это API для чекера!"


@app.route("/api/v1.0/conversion_rate/", methods=["GET"])
def get_conversion_rate():
    #json_data = {"in_timestamp":str(timestamp)}
    datetime_now = datetime.datetime.now()
    timestamp = int(
        time.mktime(datetime_now.timetuple()) * 1e3 + datetime_now.microsecond / 1e3
    )
    headers = {"Content-Type": "application/json"}
    url = app.config["POSTGREST_API_URL"]+"conversion_rate"
    res = requests.post(
        url=url,
        #data=json.dumps(json_data),
        headers=headers,
    )
    data = {
        "timestamp": timestamp,
        "contents": json.loads(res.text),
        "check": True,
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run()
