# from kafka import KafkaConsumer
from confluent_kafka import Consumer, KafkaError
from fastavro import schemaless_reader
from io import BytesIO
import json


KAFKA_URL='de3-00-kafka.loveflorida88.online:6667'
KAFKA_TOPIC='pushka_test'
KAFKA_GROUP_ID='pushka_test'

AVRO_SCHEMA_PATH="C:\\Users\\Егор\\git\\de3-team1\\silchenko\\project_02\\python\\pushka_test.avsc"

# consumer = KafkaConsumer(KAFKA_TOPIC,
#                          group_id=KAFKA_GROUP_ID,
#                          bootstrap_servers=[KAFKA_URL],
#                          auto_offset_reset="earliest",
#                          enable_auto_commit=True)
consumer = Consumer({'bootstrap.servers': KAFKA_URL,
                     'group.id': KAFKA_GROUP_ID,
                     'default.topic.config': {'auto.offset.reset': 'earliest'}
                     }
                    )
consumer.subscribe([KAFKA_TOPIC])

schema = json.load(open(AVRO_SCHEMA_PATH))

def deserialize(schema, binary):
    bytes_writer = BytesIO()
    bytes_writer.write(binary)
    bytes_writer.seek(0)
    data = schemaless_reader(bytes_writer, schema)
    return data

running = True

messages = []
while running:
    message = consumer.poll()
    if message:
        if not message.error():
            messages.append(deserialize(schema, message.value()))
            print(deserialize(schema, message.value()))
        elif message.error().code() == KafkaError._PARTITION_EOF:
            print(message.error())
            running = False
        # if len(messages) > (10 ^ 5):
        #     print(messages)
        #     messages = []
        #     running = False
print('end')
consumer.close()
#
# for message in consumer:
#     data = deserialize(schema, message.value)
#     print(data)

# consumer.close()
