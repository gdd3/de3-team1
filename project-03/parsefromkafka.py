import io
import avro.schema
import avro.io

from kafka import KafkaConsumer

consumer = KafkaConsumer('clicks', auto_offset_reset='earliest' \
                                 ,bootstrap_servers=['35.205.67.13:6667'] \
                                 , api_version=(0, 10), consumer_timeout_ms=1000)
schema = avro.schema.Parse(open("event.avsc", "rb").read())

for msg in consumer:
    raw_bytes = msg.value
    bytes_reader = io.BytesIO(raw_bytes)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    reader = avro.io.DatumReader(schema)
    try:
        event = reader.read(decoder)
        print(event)
    except:
        print ("error")
