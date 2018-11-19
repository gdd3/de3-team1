#!lab3_api_env/bin/python
from flask import Flask
from flask.json import jsonify
from prometheus_client.parser import text_string_to_metric_families
import math
import time
import requests


METRICS_PORT = 8013


app = Flask(__name__)
    
    
def get_conversion():
    r = requests.get('http://localhost:'+str(METRICS_PORT))
    page = r.content.decode('utf8')
    metrics = {}
    for family in text_string_to_metric_families(page):
        for sample in family.samples:
            if sample[0] == 'conversion':
                metrics[sample[0]] = sample[2]
    return metrics['conversion']/100


@app.route('/api/v1.0/conversion_rate/', methods=['GET'])
def api_get_conversion():
    timestamp = math.floor(time.time())
    conversion = get_conversion()
    return jsonify({
        'timestamp': timestamp,
        'contents': [
            {
                'conversion_rate': conversion
            }
        ],
        'check': True
    })


if __name__ == '__main__':
    app.run(debug=True,host = "0.0.0.0", port=5002)
