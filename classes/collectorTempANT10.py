__author__ = 'Alexey Y Manikin'

# https://github.com/Thinary/AHT10/blob/master/src/Thinary_AHT10.cpp
# https://myhydropi.com/raspberry-pi-i2c-temperature-sensor
# i2cdetect -y 0

import os
import os.path
import psutil
from abc import ABC, abstractmethod
from config.mail import *
from helpers.helpers import file_get_contents, get_hostname
from helpers.colorHelpers import BColor
from classes.collectorBase import CollectorBase
import smbus
import time

"""
I2C sensor
"""


class CollectorTempANT10(CollectorBase):

    def __init__(self, sensor_name: str, database: str):
        CollectorBase.__init__(self, sensor_name, database)

    @staticmethod
    def get_info() -> (str, str):
        bus = smbus.SMBus(1)
        config = [0x08, 0x00]
        bus.write_i2c_block_data(0x38, 0xE1, config)
        time.sleep(1)
        byt = bus.read_byte(0x38)
        #print(byt&0x68)
        MeasureCmd = [0x33, 0x00]
        bus.write_i2c_block_data(0x38, 0xAC, MeasureCmd)
        time.sleep(0.5)
        data = bus.read_i2c_block_data(0x38,0x00)
        #print(data)
        temp = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
        ctemp = ((temp*200) / 1048576) - 50
        #print(u'Temperature: {0:.1f}C'.format(ctemp))
        tmp = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
        #print(tmp)
        ctmp = int(tmp * 100 / 1048576)
        #print(u'Humidity: {0}%'.format(ctmp))
        return '{0:.1f}'.format(ctemp), '{0}'.format(ctmp)

    def get_json(self) -> dict:
        temp, humidity = 0, 0
        try:
            temp, humidity = self.get_info()
        except:
            BColor.error("Error get data from sensir %s" % self.sensor_name)
            return []

        json_body = [
            {
                "measurement": "temperature",
                "tags": {
                    "name": self.sensor_name
                },
                "fields": {
                    "temperature": float(temp),
                    "humidity": float(humidity)
                }
            }
        ]

        BColor.process("Temperature sensor %s is %s (%s)" % (self.sensor_name, temp, humidity))
        return json_body
