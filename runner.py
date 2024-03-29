__author__ = 'Alexey Y Manikin'

import sys

import schedule
import time
from config.mail import *
from helpers.colorHelpers import BColor
from helpers.helpers import check_program_run, get_hostname
from classes.collectorRaspberry import CollectorRaspberry
from classes.collectorTempDS18B20 import CollectorTempDS18B20
from classes.collectorTempANT10 import CollectorTempANT10
from classes.collectorSenseHat import CollectorSenseHat
from classes.collectorGps import CollectorGps


PROGRAM_NAME = 'runner'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, CURRENT_DIR)

if __name__ == "__main__":
    try:
        if check_program_run(PROGRAM_NAME):
            BColor.error("Program %s already running" % PROGRAM_NAME)
            sys.exit(1)

        sensorSenseHat = CollectorGps("Gps", "home")
        sensorSenseHat.start(10)
        sensorSenseHat.run()

        sensorSenseHat = CollectorSenseHat("SenseHat", "home")
        sensorSenseHat.start(5)
        sensorSenseHat.run()

        sensorRaspberry = CollectorRaspberry("raspberry_pi", "home")
        sensorRaspberry.start(30)
        sensorRaspberry.run()

        # sensorLivingRoom = CollectorTempDS18B20("sleeping_room", "28-3c01d6076425", "home")
        # sensorLivingRoom.start(1)
        # sensorLivingRoom.run()
        #
        # sensorLivingRoom2 = CollectorTempANT10("sleeping_room2",  "home")
        # sensorLivingRoom2.start(1)
        # sensorLivingRoom2.run()

        while True:
            schedule.run_pending()
            time.sleep(1)

    except KeyboardInterrupt:
        print('Ctrl C - goodbye')
    except Exception as e:
        print((traceback.format_exc()))
