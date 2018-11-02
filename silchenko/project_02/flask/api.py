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


@app.route("/api/v1.0/orders/<int:timestamp>", methods=["GET"])
def get_orders(timestamp):
    if timestamp < 940312918:
        abort(404)
    json_data = {"in_timestamp":str(timestamp)}
    headers = {"Content-Type": "application/json"}
    url = app.config["POSTGREST_API_URL"]+"orders"
    res = requests.post(
        url=url,
        data=json.dumps(json_data),
        headers=headers,
    )
    data = {
        "timestamp": timestamp,
        "contents": json.loads(res.text),
        "check": True,
    }
    return jsonify(data)


@app.route("/api/v1.0/orders/", methods=["GET"])
def get_orders_hour_ago():
    hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
    timestamp = int(
        time.mktime(hour_ago.timetuple()) * 1e3 + hour_ago.microsecond / 1e3
    )
    json_data = {"in_timestamp":str(timestamp)}
    headers = {"Content-Type": "application/json"}
    url = app.config["POSTGREST_API_URL"]+"orders"
    res = requests.post(
        url=url,
        data=json.dumps(json_data),
        headers=headers,
    )
    data = {
        "timestamp": timestamp,
        "contents": json.loads(res.text),
        "check": True,
    }
    return jsonify(data)


@app.route("/api/v1.0/users/<int:timestamp>", methods=["GET"])
def get_users(timestamp):
    if timestamp < 940312918:
        abort(404)
    json_data = {"in_timestamp":str(timestamp)}
    headers = {"Content-Type": "application/json"}
    url = app.config["POSTGREST_API_URL"]+"users"
    res = requests.post(
        url=url,
        data=json.dumps(json_data),
        headers=headers,
    )
    data = {
        "timestamp": timestamp,
        "contents": json.loads(res.text),
        "check": True,
    }
    return jsonify(data)


@app.route("/api/v1.0/users/", methods=["GET"])
def get_users_hour_ago():
    hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
    timestamp = int(
        time.mktime(hour_ago.timetuple()) * 1e3 + hour_ago.microsecond / 1e3
    )
    json_data = {"in_timestamp":str(timestamp)}
    headers = {"Content-Type": "application/json"}
    url = app.config["POSTGREST_API_URL"]+"users"
    res = requests.post(
        url=url,
        data=json.dumps(json_data),
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
