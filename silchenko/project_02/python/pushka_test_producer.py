from kafka import KafkaProducer
from fastavro import schemaless_writer
from io import BytesIO
from random import randint
import json
import time


KAFKA_URL='de3-00-kafka.loveflorida88.online:6667'
KAFKA_TOPIC='pushka_test'
AVRO_SCHEMA_PATH="C:\\Users\\Егор\\git\\de3-team1\\silchenko\\project_02\\python\\pushka_test.avsc"

input_data = [
{"product": "bulki", "time": 1245678954, "price": 100, "desc": "Fresh bulki"},
{"product": "baton", "time": 3456789012, "price": 200, "desc": "Fresh baton"},
{"product": "baget", "time": 6789012345, "price": 300, "desc": "Fresh baget"},
{"product": "kulik", "time": 8901234567, "price": 400, "desc": "Fresh kulik"},
{"product": "kakah", "time": 8765432101, "price": 500, "desc": "Fresh kakah"}
]

producer = KafkaProducer(bootstrap_servers=[KAFKA_URL])
schema = json.load(open(AVRO_SCHEMA_PATH))

for x in range(100):
    bytes_writer = BytesIO()
    schemaless_writer(bytes_writer, schema, input_data[randint(0, 4)])
    raw_bytes = bytes_writer.getvalue()
    producer.send(KAFKA_TOPIC, raw_bytes)
    # time.sleep(1)
