from kafka import KafkaProducer
from io import BytesIO
import fastavro
import json
import random
import time

TOPIC = 'events'
# KAFKA_BROKERS = ["35.233.8.138:6667"]
KAFKA_BROKERS = ["localhost:9092"]

def serialize(schema, data):
    bytes_writer = BytesIO()
    fastavro.schemaless_writer(bytes_writer, schema, data)
    return bytes_writer.getvalue()

if __name__ == '__main__':

    schema = json.load(open('avro/CheckoutEvent.avsc'))
    # schema = json.load(open('avro/sample.avsc'))

    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKERS)

    # records = [
    #     {'station': 'blabla', 'temp': 5, 'time': 1433269388},
    #     {'station': 'hello', 'temp': 22, 'time': 1433270389},
    #     {'station': 'world', 'temp': -11, 'time': 1433273379},
    #     {'station': 'coca-cola', 'temp': 111, 'time': 1433275478},
    # ]

    records = []
    for line in open("sample_producer_data.json"):
        records.append(json.loads(line))

    # for _ in range(10000):
    #     record = random.choice(records)
    #     print(f"Send: {record}")
    #     producer.send(TOPIC, serialize(schema, record))
    #     time.sleep(2)

    for record in records:
        print(f"Send: {record}")
        producer.send(TOPIC, serialize(schema, record))
        time.sleep(2)
