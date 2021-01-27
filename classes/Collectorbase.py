__author__ = 'Alexey Y Manikin'

from abc import ABC, abstractmethod


class CollectorBase(object):

    def __init__(self, sensor_name: str):
        self.sensor_name = sensor_name

    def run(self):
        pass

    @abstractmethod
    def get_json(self):
        pass

    def write_to_influx(self, json: ):