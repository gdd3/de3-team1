import requests
import json
from flask import Flask, abort, jsonify

app = Flask(__name__)
app.config["CLICKHOUSE_API_URL"] = "http://localhost:8123/"


@app.route("/")
def hello():
    return "Это API для чекера!"


@app.route("/api/v1.0/users/<int:timestamp>", methods=["GET"])
def get_users(timestamp):
    if timestamp < 940312918:
        abort(404)
    query = (
        open("query/s.users.sql", "r")
        .read()
        .replace("{{ from_timestamp }}", str(timestamp))
    )
    res = requests.post(
        url=app.config["CLICKHOUSE_API_URL"],
        data=query,
        headers={"Content-Type": "application/octet-stream"},
    )
    data = {
        "timestamp": timestamp,
        "contents": [json.loads(line) for line in res.text.split("\n")[:-1]],
        "check": True
    }
    return jsonify(data)


@app.route("/api/v1.0/orders/<int:timestamp>", methods=["GET"])
def get_orders(timestamp):
    if timestamp < 940312918:
        abort(404)
    query = (
        open("query/s.orders.sql", "r")
        .read()
        .replace("{{ from_timestamp }}", str(timestamp))
    )
    res = requests.post(
        url=app.config["CLICKHOUSE_API_URL"],
        data=query,
        headers={"Content-Type": "application/octet-stream"},
    )
    data = {
        "timestamp": timestamp,
        "contents": [json.loads(line) for line in res.text.split("\n")[:-1]],
        "check": True
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run()
