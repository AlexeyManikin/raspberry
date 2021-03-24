__author__ = 'Alexey Y Manikin'

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
        self.sense = SenseHat(imu_settings_file="RTIMULib.ini")

    def get_json(self) -> list:
        fields = {}

        humidity = self.sense.get_humidity()
        BColor.info("Humidity: %s %%rH" % humidity)
        fields['humidity'] = float(humidity)

        temp_hum = self.sense.get_temperature_from_humidity()
        BColor.info("Temperature: %s C" % temp_hum)
        fields['temperature_hum'] = float(temp_hum)

        temp_pre = self.sense.get_temperature_from_pressure()
        BColor.info("Temperature: %s C" % temp_pre)
        fields['temperature_pre'] = float(temp_pre)

        pressure = self.sense.get_pressure()
        BColor.info("Pressure: %s Millibars" % pressure)
        fields['pressure'] = float(pressure)

        self.sense.set_imu_config(True, True, True)
        orientation_rad = self.sense.get_orientation_radians()
        BColor.info("1: p: {pitch}, r: {roll}, y: {yaw}".format(**orientation_rad))

        orientation = self.sense.get_orientation_degrees()
        BColor.info("2: p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))
        fields['orientation_degrees_pitch'] = float(orientation['pitch'])
        fields['orientation_degrees_roll'] = float(orientation['roll'])
        fields['orientation_degrees_yaw'] = float(orientation['yaw'])

        orientation = self.sense.get_orientation()
        BColor.info("3: p: {pitch}, r: {roll}, y: {yaw}".format(**orientation))

        north = self.sense.get_compass()
        BColor.info("North: %s" % north)
        fields['compass_north'] = float(north)

        raw = self.sense.get_compass_raw()
        BColor.info("x: {x}, y: {y}, z: {z}".format(**raw))

        gyro_only = self.sense.get_gyroscope()
        BColor.info("p: {pitch}, r: {roll}, y: {yaw}".format(**gyro_only))
        fields['gyroscope_pitch'] = float(gyro_only['pitch'])
        fields['gyroscope_roll'] = float(gyro_only['roll'])
        fields['gyroscope_yaw'] = float(gyro_only['yaw'])

        raw = self.sense.get_gyroscope_raw()
        BColor.info("x: {x}, y: {y}, z: {z}".format(**raw))

        accel_only = self.sense.get_accelerometer()
        BColor.info("p: {pitch}, r: {roll}, y: {yaw}".format(**accel_only))
        fields['accelerometer_pitch'] = float(accel_only['pitch'])
        fields['accelerometer_roll'] = float(accel_only['roll'])
        fields['accelerometer_yaw'] = float(accel_only['yaw'])

        raw = self.sense.get_accelerometer_raw()
        BColor.info("x: {x}, y: {y}, z: {z}".format(**raw))

        json_body = [
            {
                "measurement": "sense_hat",
                "tags": {
                    "id": "sense_hat",
                    "name": "sense_hat"
                },
                "fields": fields
            }
        ]

        return json_body
