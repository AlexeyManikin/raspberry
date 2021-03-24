__author__ = 'Alexey Y Manikin'

from helpers.colorHelpers import BColor
from classes.collectorBase import CollectorBase
import RPi.GPIO as GPIO
import serial
import time
import traceback
import datetime

"""
https://www.elecrow.com/download/SIM800%20Series_GNSS_Application%20Note%20V1.00.pdf
"""


class CollectorGps(CollectorBase):

    def __init__(self, sensor_name: str, database: str):
        self.ser = serial.Serial('/dev/ttyS0', 115200)
        self.ser.flushInput()

        self.power_key = 4
        self.rec_buff = ''
        self.rec_buff2 = ''
        self.time_count = 0

        CollectorBase.__init__(self, sensor_name, database)
        self.power_on(self.power_key)

        BColor.info("Start GPS session...")
        self.send_at('AT+CGNSPWR=1', 'OK', 1)
        time.sleep(2)

    def __del__(self):
        if self.ser is not None:
            self.ser.close()
        self.power_down(self.power_key)
        GPIO.cleanup(self.power_key)

    def send_at(self, command: str, back: str, timeout: int) -> (bool, str):
        rec_buff = ''
        self.ser.write((command + '\r\n').encode())
        time.sleep(timeout)
        if self.ser.inWaiting():
            time.sleep(0.01)
            rec_buff = self.ser.read(self.ser.inWaiting())
        if rec_buff != '':
            if back not in rec_buff.decode():
                BColor.error("%s ERROR, back: %s" % (command, rec_buff.decode()))
                return False, rec_buff
            else:
                BColor.info("command %s -> %s" % (command, rec_buff.decode()))
                return True, rec_buff
        else:
            BColor.warning("GPS is not ready")
            return False, rec_buff

    @staticmethod
    def format_answer(raw_buff: bytes) -> str:
        input_string = "".join(map(chr, raw_buff))
        start_string = 'AT+CGNSINF\r\r\n+CGNSINF: '
        end_string = '\r\n\r\nOK\r\n'
        if start_string in input_string:
            input_string = input_string[len(start_string):]
        if end_string in input_string:
            input_string = input_string[:len(input_string) - len(end_string)]
        return input_string

    def get_gps_position(self) -> str:
        answer, rec_buff = self.send_at('AT+CGNSINF', '+CGNSINF: ', 1)
        if answer:
            if b',,,,,,' in rec_buff:
                BColor.warning('GPS is not ready')
                time.sleep(1)
            return self.format_answer(rec_buff)
        else:
            BColor.error('error %d' % answer)
            self.send_at('AT+CGPS=0', 'OK', 1)
            return ''

    def power_on(self, power_key):
        BColor.info('SIM7600X is starting:')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(power_key, GPIO.OUT)
        time.sleep(0.1)
        GPIO.output(power_key, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(power_key, GPIO.LOW)
        time.sleep(2)
        self.ser.flushInput()
        BColor.info('SIM7600X is ready')

    def power_down(self, power_key):
        BColor.info('SIM7600X is loging off:')
        GPIO.output(power_key, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(power_key, GPIO.LOW)
        time.sleep(2)
        BColor.info('Good bye')

    def parce_CGNSINF(self, input_string: str) -> dict:
        splited_string = input_string.split(",")
        gps_info = {}

        try:
            gps_info['GPS_run_status'] = bool(splited_string[0])
            gps_info['Fix_status'] = bool(splited_string[1])
            gps_info['UTC_date'] = time.mktime(
                datetime.datetime.strptime(splited_string[2], '%Y%m%d%H%M%S.%f').timetuple())
            gps_info['Latitude'] = float(splited_string[3])
            gps_info['Longitude'] = float(splited_string[4])
            gps_info['MSL_Altitude'] = float(splited_string[5])
            gps_info['Speed_Over_Ground'] = float(splited_string[6])
            gps_info['Course_Over_Ground '] = float(splited_string[7])
            gps_info['Fix_Mode '] = int(splited_string[8])
            gps_info['Reserved1'] = splited_string[9]
            gps_info['HDOP'] = float(splited_string[10])  # https://ru.wikipedia.org/wiki/DOP
            gps_info['PDOP'] = float(splited_string[11])
            gps_info['VDOP'] = float(splited_string[12])
            gps_info['Reserved2'] = splited_string[13]
            gps_info['GPS_Satellites_in_View '] = int(splited_string[14])
            gps_info['GNSS_Satellites_Used'] = int(splited_string[15])
            gps_info['GLONASS_Satellites_in_View'] = int(splited_string[16])
            gps_info['Reserved3'] = splited_string[17]
            gps_info['C_N0_max'] = int(splited_string[18])
            gps_info['HPA'] = float(splited_string[19])
            gps_info['VPA'] = float(splited_string[20])
        except:
            return gps_info

        return gps_info

    def get_json(self) -> list:
        try:
            position = self.get_gps_position()
            json_body = [
                {
                    "measurement": "position",
                    "tags": {
                        "id": 'gps',
                        "name": 'gps_hat'
                    },
                    "fields": self.parce_CGNSINF(position)
                }
            ]
            return json_body
        except Exception as e:
            print((traceback.format_exc()))
            return []
