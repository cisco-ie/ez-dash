#!/usr/bin/env python3
import threading
import logging
import math
import time
import random
import sys
import prometheus_client as prometheus


REQUEST_TIME = prometheus.Summary('request_processing_seconds', 'Time spent processing request')

def main():
    """Entry point to example app."""
    setup_logging(logging.DEBUG)
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
        stat_1, stat_2 = stat_creation(count)
        influx_controller.send_data(stat_1, stat_2, count)
        count += 1
        time.sleep(1)

@REQUEST_TIME.time()
def stat_creation(i):
    """Create a sinusoidal/random integer statistic."""
    stat_1 = 10 + math.sin(math.radians(i)) * 50
    stat_2 = random.randint(0, 200)
    return stat_1, stat_2


import requests
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
            raise
        if response.status_code != 204:
            logging.error(response.text)

    def format_data(self, key, value):
        timestamp = int(round(time.time() * 1000)) # Milliseconds
        data = "{key},host=python value={value} {timestamp}".format(
            key=key,
            value=value,
            timestamp=timestamp
        )
        return data

    def send_data(self, stat_1, stat_2, stat_3):
        self.write(self.format_data('stat_1', stat_1))
        self.write(self.format_data('stat_2', stat_2))
        self.write(self.format_data('entries_counter', stat_3))

if __name__ == '__main__':
    main()
