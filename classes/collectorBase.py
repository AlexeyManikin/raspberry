__author__ = 'Alexey Y Manikin'

from abc import ABC, abstractmethod
import influxdb
import schedule
import time
from helpers.helpers import get_hostname
import traceback


class CollectorBase(object):

    def __init__(self, sensor_name: str, database: str):
        self.sensor_name = sensor_name
        self.database = database
        self.run_status = 0

    def run(self):
        if self.run_status == 0:
            print("done")
            return schedule.CancelJob

        try:
            json = self.get_json()
            self.write_to_influx(json)
        except Exception as e:
            print((traceback.format_exc()))

    def write_to_influx(self, json: dict) -> bool:
        client = influxdb.InfluxDBClient(host='localhost', port=8086)
        client.switch_database(self.database)
        if client.write_points(json):
            return True
        return False

    def start(self, time: int):
        self.run_status = 1
        schedule.every(time).seconds.do(self.run)

    def stop(self):
        self.run_status = 0

    @abstractmethod
    def get_json(self) -> list:
        pass
