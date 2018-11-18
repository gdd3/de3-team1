#!lab2_env/bin/python
from flask import Flask
from flask.json import jsonify
import psycopg2
import psycopg2.extras
import math
import time


app = Flask(__name__)


SQL_QUERIES = {
    'users': """SELECT url,item_id AS "id_item",SUM(count) AS count, AVG(deep) AS deep FROM users WHERE ts >= {} GROUP BY item_id,url;""",
    'orders': """SELECT url,item_id AS "id_item",SUM(count) AS count, SUM(sum) AS sum FROM orders WHERE ts >= {} GROUP BY item_id,url;"""
}


def dbc():
    db_name = 'online_shop'
    db_user = 'online_shop'
    db_pass = 'password'
    db_host = 'localhost'
    db_port = '5432'
    con = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
    cur = con.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    return con,cur
    
    
def get_info(query_type,timestamp):
    timestamp = int(timestamp)

    con,cur = dbc()
    cur.execute(SQL_QUERIES[query_type].format(timestamp))
    
    result = {
        'timestamp': timestamp,
        'contents': [],
        'check': True
    }
    records = cur.fetchall()
    for record in records:
        result['contents'].append(record)
    con.close()
        
    return result


@app.route('/api/v1.0/users', methods=['GET'])
def api_get_users():
    timestamp = math.floor(time.time()) - 60*60
    users = get_info('users',timestamp)
    return jsonify(users)

@app.route('/api/v1.0/users/<int:timestamp>', methods=['GET'])
def api_get_users_by_timestamp(timestamp):
    users = get_info('users',timestamp)
    return jsonify(users)

@app.route('/api/v1.0/orders', methods=['GET'])
def api_get_orders():
    timestamp = math.floor(time.time()) - 60*60
    orders = get_info('orders',timestamp)
    return jsonify(orders)

@app.route('/api/v1.0/orders/<int:timestamp>', methods=['GET'])
def api_get_orders_by_timestamp(timestamp):
    orders = get_info('orders',timestamp)
    return jsonify(orders)


if __name__ == '__main__':
    app.run(host = "0.0.0.0", port=5001)
