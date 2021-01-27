__author__ = 'Alexey Y Manikin'

import sys

from config.mail import *
from helpers.helpers import file_get_contents, check_program_run, get_hostname
import influxdb

PROGRAM_NAME = 'temperature'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, CURRENT_DIR)

if __name__ == "__main__":
    try:
        if check_program_run(PROGRAM_NAME):
            BColor.error("Program %s already running" % PROGRAM_NAME)
            sys.exit(1)
        client = InfluxDBClient(host='localhost', port=8086)
        client.switch_database('home')
        temperature = file_get_contents("/sys/class/thermal/thermal_zone0/temp")
        json_body = [
            {
                "measurement": "cputemp",
                "tags": {
                    "computer": "raspberry pi 3",
                    "hostname": get_hostname()
                },
                "fields": {
                    "value_temperature": int(temperature)/1000
                }
            }
        ]

        client.write_points(json_body)
        print(int(temperature)/1000)
    except Exception as e:
        print((traceback.format_exc()))
