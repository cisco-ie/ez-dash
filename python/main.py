from prometheus_client import start_http_server, Summary
import threading
import math
import time
import random
import sys
import http.client

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


def main():
    """
    Runs all functions required for exposing
    """

    try:
        print("Starting Prometheus Server")
        prometheus_server()
        print("Starting Influx Server")
        t = threading.Thread(target=influx_server)
        t.start()

    except KeyboardInterrupt:
        sys.exit()


def prometheus_server():
    start_http_server(9091)


def influx_server():
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
        # print(res.code)
        print(data.decode("utf-8"))

    def format_data(self, key, value):
        timestamp = int(time.time()) * 1000000000
        data = "{},host=python value={} {}".format(key, value, timestamp)
        # print(data)
        return data

    def send_data(self, stat_1, stat_2, stat_3):
        self.write(self.format_data('stat_1', stat_1))
        self.write(self.format_data('stat_2', stat_2))
        self.write(self.format_data('entriest_counter', stat_3))


if __name__ == '__main__':
    main()
