#!/usr/bin/env python3
import threading
import logging
import math
import time
import random
import sys
import http.client
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
    influx_controller = InfluxController('influxdb:8086')
    while True:
        stat_1, stat_2 = stat_creation(count)
        influx_controller.send_data(stat_1, stat_2, count)
        count += 1
        time.sleep(1)

@REQUEST_TIME.time()
def stat_creation(i):
    stat_1 = 10 + math.sin(math.radians(i)) * 50
    stat_2 = random.randint(0, 200)
    return stat_1, stat_2

class InfluxController():
    def __init__(self, url, dbname='ezdash'):
        self.dbname = dbname
        self.conn = http.client.HTTPConnection(url)

    def write(self, payload):
        headers = {
            'authorization': "Basic ZGV2bmV0OmNyZWF0ZQ=="
        }
        self.conn.request("POST", "/write?db={}".format(self.dbname), payload, headers)
        res = self.conn.getresponse()
        data = res.read()
        logging.debug(data.decode("utf-8"))

    def format_data(self, key, value):
        timestamp = int(round(time.time() * 1e9)) # Nanoseconds
        data = "{key},host=python value={value} {timestamp}".format(
            key=key,
            value=value,
            timestamp=timestamp
        )
        return data

    def send_data(self, stat_1, stat_2, stat_3):
        self.write(self.format_data('stat_1', stat_1))
        self.write(self.format_data('stat_2', stat_2))
        self.write(self.format_data('entriest_counter', stat_3))

if __name__ == '__main__':
    main()
