import requests
import json
import time
import datetime
from flask import Flask, abort, jsonify

app = Flask(__name__)
app.config["CLICKHOUSE_API_URL"] = "http://localhost:8123/"


@app.route("/")
def hello():
    return "Это API для чекера!"


@app.route("/api/v1.0/conversion_rate/", methods=["GET"])
def get_orders_hour_ago():
    query = open("query/s.conversion.sql", "r").read()

    res = requests.post(
        url=app.config["CLICKHOUSE_API_URL"],
        data=query,
        headers={"Content-Type": "application/octet-stream"},
    )
    data = {
        "timestamp": 940312910,
        "contents": json.loads(res.text),
        "check": True,
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run()
