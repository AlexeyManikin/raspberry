__author__ = 'Alexey Y Manikin'

import os.path
from config.mail import *
from helpers.helpers import file_get_contents
from helpers.colorHelpers import BColor
from classes.collectorBase import CollectorBase

"""
1Wire sensor
"""


class CollectorTempDS18B20(CollectorBase):

    def __init__(self, sensor_name: str, sensor_id: str, database: str):
        CollectorBase.__init__(self, sensor_name, database)
        self.sensor_id = sensor_id
        self.sensor_data_name = os.path.abspath("/sys/bus/w1/devices/%s/temperature" % self.sensor_id)

    def get_json(self) -> list:
        if not os.path.exists(self.sensor_data_name):
            BColor.error("Sensor %s file %s not exist" % (self.sensor_name, self.sensor_data_name))
            return []

        temperature = file_get_contents(self.sensor_data_name)

        json_body = [
            {
                "measurement": "temperature",
                "tags": {
                    "id": self.sensor_id,
                    "name": self.sensor_name
                },
                "fields": {
                    "temperature": int(temperature) / 1000
                }
            }
        ]

        BColor.process("Temperature sensor %s is %s" % (self.sensor_name, str(int(temperature) / 1000)))
        return json_body
