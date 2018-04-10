#!/usr/bin/env python
"""Simple Python application which exposes metrics to Prometheus
and InfluxDB to populate pre-configured dashboards in Grafana.
"""
import logging
import math
import time
import random
import requests
import threading
import prometheus_client as prometheus
from flask import Flask

app = Flask(__name__)
REQUEST_TIME = prometheus.Summary('request_processing_seconds', 'Time spent processing request')
APP_Gauge = prometheus.Gauge('flask_gauge', 'Flask input changing gauge')


def main():
    """Entry point to example app."""
    setup_logging(logging.DEBUG)
    logging.info('Starting Flask Server')
    threading.Thread(target=start_flask).start()
    logging.info('Starting Prometheus Server')
    start_prometheus()
    logging.info('Starting metrics generation to InfluxDB')
    start_metrics()



def setup_logging(level=logging.INFO):
    """Setup logging to output to standard out."""
    logging.basicConfig(level=level)
    logging.getLogger('urllib3').setLevel(logging.WARNING)


def start_prometheus(port=9091):
    """Start the Prometheus HTTP server."""
    prometheus.start_http_server(port)


def start_metrics():
    """Start generating metrics into InfluxDB."""
    count = 1
    influx_controller = InfluxController('http://influxdb:8086', 'devnet', 'create')
    while True:
        stats = {
            'sinwave': calculate_sinwave(count),
            'gauge': calculate_gauge(),
            'counter': count
        }
        influx_controller.send_data(stats)
        count += 1
        time.sleep(1)


def start_flask():
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
    return


@app.route('/')
def flask_app():
    return 'Welcome to DevNet Create'


@app.route('/up')
def flask_gauge_up():
    APP_Gauge.inc()
    return 'Incremented to {}'.format(APP_Gauge._value.get())


@app.route('/down')
def flask_gauge_down():
    APP_Gauge.dec()
    return 'Decremented to {}'.format(APP_Gauge._value.get())


@REQUEST_TIME.time()
def calculate_sinwave(i):
    """Create a sinusoidal statistic."""
    return 10 + math.sin(math.radians(i)) * 50


def calculate_gauge():
    """Create fixed range statistic for gauge."""
    return random.randint(0, 100)


class InfluxController():
    """Custom class for writing data points to the InfluxDB HTTP API
    due to Python client library not supporting versions above 1.3.
    """

    def __init__(self, url, username, password, dbname='ezdash'):
        """Initialize with a URL, username, password, and database name."""
        self.url = url
        self.username = username
        self.password = password
        self.dbname = dbname
        self.conn = requests.Session()

    def write(self, payload):
        """Write to InfluxDB via HTTP API.
        Effectively ripped from:
        https://github.com/influxdata/influxdb-python/blob/master/influxdb/client.py#L243
        https://docs.influxdata.com/influxdb/v1.5/tools/api/#write
        """
        try:
            response = self.conn.request(
                method='POST',
                url=self.url + '/write',
                auth=(self.username, self.password),
                params={'db': self.dbname, 'precision': 'ms'},
                data=payload
            )
        except (requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError,
                requests.exceptions.Timeout):
            logging.error("Failed to connect")
            time.sleep(2)
        if response.status_code != 204:
            logging.error(response.text)

    def format_data(self, key, value):
        """Format data to InfluxDB line format."""
        timestamp = int(round(time.time() * 1000)) # Milliseconds
        data = "{key},host=python value={value} {timestamp}".format(
            key=key,
            value=value,
            timestamp=timestamp
        )
        return data
    
    def send_data(self, kv_map):
        """Send a KV map of data to InfluxDB for series storage."""
        for key, value in kv_map.items():
            self.write(
                self.format_data(key, value)
            )

if __name__ == '__main__':
    main()
