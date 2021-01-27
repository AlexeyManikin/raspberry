import os
import traceback
from influxdb import InfluxDBClient

_author__ = 'alexeyymnaikin'

# Default logger
CURRENT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)) + '/../')
