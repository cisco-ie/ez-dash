from influxdb import InfluxDBClient
from prometheus_client import start_http_server, Summary
import threading
import math
import time
import datetime
import random
import sys

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


def main():
    """
    Runs all functions required for exposing
    """
    # influx_controller = InfluxController()
    # influx_controller.setup_db()
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
    # influx_controller = InfluxController()
    while True:
        stat_1, stat_2 = stat_creation(count)
        # influx_controller.send_data(stat_1, stat_2, count)
        count += 1
        time.sleep(1)


@REQUEST_TIME.time()
def stat_creation(i):
    stat_1 = 10 + math.sin(math.radians(i)) * 10
    stat_2 = random.randint(0, 200)
    return stat_1, stat_2


class InfluxController():
    def __init__(self, host='influxdb', port=8086, user='root', password='root', dbname='tutorial'):
        """
        Need to add in static route
        """
        self.dbname = dbname
        self.client = InfluxDBClient(host, port, user, password, dbname)

    def setup_db(self):
        self.client.create_database(self.dbname)

    def write_to_db(self, points):
        self.client.switch_database(self.dbname)
        self.write_points(points)

    def format_data(self, metric, value):
        now = datetime.datetime.today()
        point = {
            "measurement": metric,
            "time": int(now.strftime('%s')),
            "fields": {
                "value": value
            }
        }
        return point

    def send_data(self, stat_1, stat_2, stat_3):
        points = []
        points.append(self.format_data('app_data.stat_1', stat_1))
        points.append(self.format_data('app_data.stat_2', stat_2))
        points.append(self.format_data('app_data.entries_counter', stat_3))
        self.write_to_db(points)

    def cleanup(self):
        self.client.drop_database(self.dbname)


if __name__ == '__main__':
    main()
