# -*- coding: UTF-8 -*-
import re
import datetime
import io
from kafka import KafkaConsumer
from avro.io import DatumReader, BinaryDecoder
import avro.schema
from prometheus_client import start_http_server, Gauge


SCHEMA_PATH = ''
TOPIC_NAME = ''
GROUP_ID = ''
BOOTSTRAP_SERVERS = ['ip:port']
RAW_METRICS_PORT = 8012
METRICS_DEFAULT = {
    'last_message_time': 0,
    'users_count': 0,
    'orders_count': 0,
    'conversion': 0.0,
    'aov': 0.0,
    'tov': 0.0
}


def avro_deserializer(data,reader):
    bytes_reader = io.BytesIO(data)
    decoder = BinaryDecoder(bytes_reader)
    result = reader.read(decoder)
    return result

def price_convert(price_str):
    return float(re.sub('\D','',price_str))

def is_same_interval(ts1,ts2,interval_length):
    return ts1 // interval_length == ts2 // interval_length

def recalc_avg(avg,new_value):
    return ((avg[0] * avg[1] + new_value) / (avg[1] + 1), avg[1] + 1)


if __name__ == '__main__':
    # делаем ридер для авро-схема
    schema = avro.schema.Parse(open(SCHEMA_PATH,'r').read())
    reader = DatumReader(schema)

    # создаем консьюмера
    consumer = KafkaConsumer(
        TOPIC_NAME,
        group_id=GROUP_ID,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        api_version=(0, 10),
        auto_offset_reset='latest',
        enable_auto_commit=True
    )

    # prometheus
    gauges = {x:Gauge(x,'') for x in METRICS_DEFAULT}
    for k in gauges: 
        gauges[k].set(METRICS_DEFAULT[k])
    start_http_server(RAW_METRICS_PORT)

    # default values
    last_message_time = 0
    users = set() # пользователи в пятиминутке последнего сообщения
    conversion_users = set() # пользователи за час последнего сообщения
    conversion_users_orders = set() # пользователи, которые сделали заказ за час последнего сообщения
    average_order_value = (0, 0) # средний чек за сутки последнего сообщения

    # читаем сообщения и генерируем сырые метрики
    try:
        for message in consumer:
            data = avro_deserializer(message.value,reader)
            print(data)
            current_time = data['timestamp']
            current_user = data['sessionId']
            current_event = data['eventType']

            if not is_same_interval(current_time,last_message_time,8.64e7):
                average_order_value = (0, 0)
                gauges['tov'].set(0.0)
                gauges['aov'].set(0.0)
            if not is_same_interval(current_time,last_message_time,3.6e6):
                conversion_users = set()
                conversion_users_orders = set()
                gauges['conversion'].set(0.0)
            if not is_same_interval(current_time,last_message_time,3e5):
                users = set()
                gauges['orders_count'].set(0)

            last_message_time = current_time
            gauges['last_message_time'].set(current_time)
            users.add(current_user)
            gauges['users_count'].set(len(users))
            conversion_users.add(current_user)
            if current_event == 'checkout_click':
                current_price = price_convert(data['total_price'])
                gauges['orders_count'].inc()
                conversion_users_orders.add(current_user)
                gauges['conversion'].set(round(len(conversion_users_orders) / len(conversion_users) * 100, 2))
                gauges['tov'].inc(current_price)
                average_order_value = recalc_avg(average_order_value, current_price)
                gauges['aov'].set(round(average_order_value[0], 2))
    except:
        consumer.close()
        print('closed')
        