#!/usr/bin/env python
from datetime import datetime, timedelta
from io import BytesIO
import json
import sys
import yaml
import fastavro
from confluent_kafka import Consumer, KafkaError, TopicPartition


class EventConsumer(Consumer):
    def __init__(self, conf, schema):
        super().__init__(conf)
        self.schema = schema
        self.assignment = [None]

    def on_assign(self, consumer, partitions):
        self.assignment = partitions
        sys.stderr.write("Assignment: %s\n" % partitions)

    def batch(self, timeout):
        try:
            part_eof_count = 0
            while part_eof_count < len(self.assignment):
                msg = self.poll(timeout)
                if msg:
                    if msg.error():
                        if msg.error().code() == KafkaError._PARTITION_EOF:
                            sys.stderr.write(
                                "%% %s [%d] reached end at offset %d\n"
                                % (msg.topic(), msg.partition(), msg.offset())
                            )
                            part_eof_count += 1
                        else:
                            raise KafkaException(msg.error())
                    else:
                        print(json.dumps(self.deserialize(msg.value())))
                else:
                    continue

        except KeyboardInterrupt:
            sys.stderr.write("%% Aborted by user\n")

        finally:
            self.close()

    def deserialize(self, binary):
        bytes_writer = BytesIO()
        bytes_writer.write(binary)
        bytes_writer.seek(0)
        return fastavro.schemaless_reader(bytes_writer, self.schema)


if __name__ == "__main__":

    with open("conf/event_consumer.yml", "r") as ymlfile:
        conf = yaml.load(ymlfile)

    ec = EventConsumer(
        conf=conf["consumer"], schema=json.load(open(conf["avro_schema"]))
    )
    ec.subscribe(conf["topics"], on_assign=ec.on_assign)
    ec.batch(conf["timeout"])
