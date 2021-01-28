__author__ = 'Alexey Y Manikin'

import os
import os.path
import psutil
from abc import ABC, abstractmethod
from config.mail import *
from helpers.helpers import file_get_contents, get_hostname
from helpers.colorHelpers import BColor
from classes.collectorBase import CollectorBase
from sense_hat import SenseHat

"""
any ground pin
1, 2 - 3v and 5v power
3, 5 - BCM 2 and 3 - I2C
16, 18 - BCM 23 and 24 - Joystick
27, 28 - BCM 0 and 1 - EEPROM

https://www.raspberrypi.org/forums/viewtopic.php?t=118964   
https://pinout.xyz/pinout/sense_hat#
https://www.raspberrypi.org/app/uploads/2015/08/Sense-HAT-V1_0.pdf
https://github.com/RPi-Distro/RTIMULib/blob/b949681af69b45f0f7f4bb53b6770037b5b02178/Linux/python/README.md

https://github.com/mrbichel/RTIMULib

apt-get install python-dev python3-dev libxml2-dev libxslt1-dev zlib1g-dev libsasl2-dev libldap2-dev 
build-essential libssl-dev libffi-dev libmysqlclient-dev libjpeg-dev libpq-dev libjpeg8-dev liblcms2-dev 
libblas-dev libatlas-base-dev 
"""


class CollectorSenseHat(CollectorBase):

    def __init__(self, sensor_name: str, database: str):
        CollectorBase.__init__(self, sensor_name, database)

    def get_json(self) -> dict:

        sense = SenseHat(imu_settings_file="RTIMULib.ini")
        humidity = sense.get_humidity()
        print("Humidity: %s %%rH" % humidity)

        temp_hum = sense.get_temperature_from_humidity()
        print("Temperature: %s C" % temp_hum)

        temp_pre = sense.get_temperature_from_pressure()
        print("Temperature: %s C" % temp_pre)

        pressure = sense.get_pressure()
        print("Pressure: %s Millibars" % pressure)

        sense.set_imu_config(True, True, True)
        orientation_rad = sense.get_orientation_radians()
        print("1: p: {pitch}, r: {roll}, y: {yaw}".format(**orientation_rad))

        orientation = sense.get_orientation_degrees()
        print("2: p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))

        orientation = sense.get_orientation()
        print("3: p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))

        north = sense.get_compass()
        print("North: %s" % north)

        raw = sense.get_compass_raw()
        print("x: {x}, y: {y}, z: {z}".format(**raw))

        gyro_only = sense.get_gyroscope()
        print("p: {pitch}, r: {roll}, y: {yaw}".format(**gyro_only))

        raw = sense.get_gyroscope_raw()
        print("x: {x}, y: {y}, z: {z}".format(**raw))

        accel_only = sense.get_accelerometer()
        print("p: {pitch}, r: {roll}, y: {yaw}".format(**accel_only))

        raw = sense.get_accelerometer_raw()
        print("x: {x}, y: {y}, z: {z}".format(**raw))
        return []
