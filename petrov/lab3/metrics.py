# -*- coding: UTF-8 -*-
import requests
import time
from prometheus_client import start_http_server, Gauge
from prometheus_client.parser import text_string_to_metric_families


RAW_METRICS_PORT = 8012
METRICS_PORT = 8013
UPDATE_INTERVAL = 5 * 60.0
RAW_METRICS = ['last_message_time','users_count','orders_count','conversion','aov','tov']
METRICS_DEFAULT = {
    'users_count': 0,
    'orders_count': 0,
    'conversion': 0.0,
    'aov': 0.0,
    'tov': 0.0
}


def is_same_interval(ts1,ts2,interval_length):
    return ts1 // interval_length == ts2 // interval_length

def update_metrics():
    r = requests.get('http://localhost:'+str(RAW_METRICS_PORT))
    page = r.content.decode('utf8')
    metrics = {}
    for family in text_string_to_metric_families(page):
        for sample in family.samples:
            if sample[0] in RAW_METRICS:
                metrics[sample[0]] = sample[2]
            
    current_time = time.time() * 1000
    last_message_time = metrics['last_message_time']
    if not is_same_interval(current_time,last_message_time,8.64e7):
        metrics['tov'] = 0.0
        metrics['aov'] = 0.0
    if not is_same_interval(current_time,last_message_time,3.6e6):
        metrics['conversion'] = 0.0
    if not is_same_interval(current_time,last_message_time,3e5):
        metrics['users_count'] = 0
        metrics['orders_count'] = 0
        
    for metric in METRICS_DEFAULT:
        gauges[metric].set(metrics[metric])
        
    print(current_time)


if __name__ == '__main__':
    gauges = {x:Gauge(x,'') for x in METRICS_DEFAULT}
    for k in gauges: 
        gauges[k].set(METRICS_DEFAULT[k])
    start_http_server(METRICS_PORT)
    start_time = time.time()
    while True:
        update_metrics()
        time.sleep(UPDATE_INTERVAL - ((time.time() - start_time) % UPDATE_INTERVAL))
