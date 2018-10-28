from kafka import KafkaConsumer

consumer = KafkaConsumer('clicks', auto_offset_reset='earliest' \
                                 ,bootstrap_servers=['35.205.67.13:6667'] \
                                 , api_version=(0, 10), consumer_timeout_ms=1000)
for msg in consumer:
    print(msg.value)
