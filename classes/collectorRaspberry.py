__author__ = 'Alexey Y Manikin'

import os
import psutil
from abc import ABC, abstractmethod
from config.mail import *
from helpers.helpers import file_get_contents, get_hostname
from helpers.colorHelpers import BColor
from classes.collectorBase import CollectorBase


class CollectorRaspberry(CollectorBase):

    def __init__(self, sensor_name: str, database: str):
        CollectorBase.__init__(self, sensor_name, database)

    def get_json(self) -> dict:
        temperature = file_get_contents("/sys/class/thermal/thermal_zone0/temp")
        load1, load5, load15 = os.getloadavg()
        mem = psutil.virtual_memory()
        hdd = psutil.disk_usage('/')

        json_body = [
            {
                "measurement": self.sensor_name,
                "tags": {
                    "computer": "raspberry pi 3",
                    "hostname": get_hostname()
                },
                "fields": {
                    "cpu_temperature": int(temperature)/1000,
                    "load1": load1,
                    "load5": load5,
                    "load15": load15,
                    "free_mem": int(mem.available/1024/1024),
                    "free_hdd": int(hdd.free / (2**30) * 1024)
                }
            }
        ]

        BColor.process("Temperature cpu is %s" % str(int(temperature)/1000))
        return json_body
