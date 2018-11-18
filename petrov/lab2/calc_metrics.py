# -*- coding: UTF-8 -*-
from kafka import KafkaConsumer
import io
from avro.io import DatumReader, BinaryDecoder
import avro.schema
import re
import time
import math
import psycopg2
import psycopg2.extras


SCHEMA_PATH = '/home/obsurder/divolte-collector-0.9.0/conf/lab2.avsc'
TOPIC_NAME = 'online_store'
GROUP_ID = 'metrics'
BOOTSTRAP_SERVERS = ['localhost:6667']


def avro_deserializer(data,reader):
    bytes_reader = io.BytesIO(data)
    decoder = BinaryDecoder(bytes_reader)
    result = reader.read(decoder)
    return result


def get_messages():
    # делаем ридер для авро-схема
    schema = avro.schema.Parse(open(SCHEMA_PATH,'r').read())
    reader = DatumReader(schema)
    
    # создаем консьюмера
    consumer = KafkaConsumer(
        TOPIC_NAME,
        group_id=GROUP_ID,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        api_version=(0, 10),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        consumer_timeout_ms=15000
    )
    
    # читаем последние сообщения
    messages = []
    for message in consumer:
        messages.append(avro_deserializer(message.value,reader))
    consumer.close()
    
    # сортируем по времени
    messages = sorted(messages, key=lambda k: k['timestamp'])
    
    return messages


def is_item(location):
    if location != 'https://b24-khpv25.bitrix24.shop/katalog/item/':
        return 'https://b24-khpv25.bitrix24.shop/katalog/item/' in location
    else:
        return False


def get_item_id(location):
    return re.findall('(?<=https:\/\/b24-khpv25\.bitrix24\.shop\/katalog\/item\/).*(?=\/)',location)[0]


def calc_metrics(messages):
    items = {}
    sessions = {}
    for message in messages:
        location = message['location']
        session_id = message['sessionId']
        event_type = message['eventType']
        sessions.setdefault(session_id,{'page_views_count':0})
        if event_type == 'pageView':
            sessions[session_id]['page_views_count'] += 1
        if is_item(location):
            item_id = get_item_id(location)
            items.setdefault(item_id,{'page_views_count':0,'deep':0.0,'orders_count':0,'orders_sum':0.0})
            if event_type == 'pageView':
                items[item_id]['page_views_count'] += 1
                t = items[item_id]['page_views_count']
                items[item_id]['deep'] = (t - 1) / t * items[item_id]['deep'] + 1 / t * sessions[session_id]['page_views_count']
            if event_type == 'buy_button_click':
                items[item_id]['orders_count'] += int(message['amount'])
                items[item_id]['orders_sum'] += float(re.sub("\D","",message['price'])) * int(message['amount'])
    return items


def dbc():
    db_name = 'online_shop'
    db_user = 'online_shop'
    db_pass = 'password'
    db_host = 'localhost'
    db_port = '5432'
    con = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
    cur = con.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    return con,cur


if __name__ == '__main__':
    messages = get_messages()
    items = calc_metrics(messages)
    ts = math.floor(time.time())
    users_records = [[ts,'b24-khpv25.bitrix24.shop',x,items[x]['page_views_count'],items[x]['deep']] for x in items]
    orders_records = [[ts,'b24-khpv25.bitrix24.shop',x,items[x]['orders_count'],items[x]['orders_sum']] for x in items if items[x]['orders_count'] != 0]
    con,cur = dbc()
    psycopg2.extras.execute_values(cur, "INSERT INTO users VALUES %s", users_records, page_size=100)
    psycopg2.extras.execute_values(cur, "INSERT INTO orders VALUES %s", orders_records, page_size=100)
    con.commit()
    con.close()
