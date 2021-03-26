__author__ = 'Alexey Y Manikin'

import psutil
from config.mail import *
from helpers.helpers import file_get_contents, get_hostname
from helpers.colorHelpers import BColor
from classes.collectorBase import CollectorBase
from subprocess import check_output
import pprint


class CollectorRaspberry(CollectorBase):

    def __init__(self, sensor_name: str, database: str):
        CollectorBase.__init__(self, sensor_name, database)

    @staticmethod
    def get_wifi_info(interface: str) -> dict:
        return_table = {"link_quality": 0, "signal_level": 0}

        # сделать нормально
        out = check_output(["/usr/sbin/iwconfig", interface])
        lines = out.split(b'  ')
        for item in lines:
            pair = item.split(b'=')
            if pair[0] == b'Link Quality':
                return_table['link_quality'] = int(pair[1].split(b'/')[0])

            if pair[0] == b'Signal level':
                return_table['signal_level'] = int(pair[1].split(b'/')[0].split(b" ")[0])
        return return_table

    def get_json(self) -> list:
        temperature = file_get_contents("/sys/class/thermal/thermal_zone0/temp")
        load1, load5, load15 = os.getloadavg()
        mem = psutil.virtual_memory()
        hdd = psutil.disk_usage('/')
        wifi = self.get_wifi_info("wlan0")

        json_body = [
            {
                "measurement": self.sensor_name,
                "tags": {
                    "computer": "raspberry pi 3",
                    "hostname": get_hostname()
                },
                "fields": {
                    "cpu_temperature": int(temperature) / 1000,
                    "load1": float(load1),
                    "load5": float(load5),
                    "load15": float(load15),
                    "free_mem": int(mem.available / 1024 / 1024),
                    "free_hdd": int(hdd.free / (2 ** 30) * 1024),
                    "link_quality": float(wifi['link_quality']),
                    "signal_level": float(wifi['signal_level'])
                }
            }
        ]

        BColor.info(pprint.pformat(json_body))

        return json_body
