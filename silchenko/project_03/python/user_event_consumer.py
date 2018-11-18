from confluent_kafka import Consumer, KafkaError
from fastavro import schemaless_reader
from io import BytesIO
import json
import sys


KAFKA_URL='de3-03-kafka.loveflorida88.online:9092'
KAFKA_TOPIC='user_event'
KAFKA_GROUP_ID='user_event_python_batch'
POLL_TIMEOUT=1.0
AVRO_SCHEMA_PATH="C:\\Users\\Егор\\git\\de3-team1\\silchenko\\project_03\\divolte\\user_event.avsc"

consumer = Consumer({'bootstrap.servers': KAFKA_URL,
                     'group.id': KAFKA_GROUP_ID,
                     'default.topic.config': {'auto.offset.reset': 'earliest'},
                     'enable.auto.commit': 'true'
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

while running:
    message = consumer.poll(POLL_TIMEOUT)
    if message:
        if not message.error():
            print(json.dumps(deserialize(schema, message.value())))
        elif message.error().code() == KafkaError._PARTITION_EOF:
            sys.stderr.write("%% %s [%d] reached end at offset %d\n"
                             % (message.topic(),
                                message.partition(),
                                message.offset()
                                )
                            )
            running = False

consumer.close()
