from datetime import datetime
import time
import pytz

CARLA_PORT = 'COM1'
VEHICLE_PORT = 'NA'
SEND_INTERVAL = 1
PACKET_COUNT = 60

# 14 floats in each half = 2(14*4) = 112 bytes
PACKET_SIZE = 112

# get time for printing only
def get_time():
    tz = pytz.timezone('America/New_York')
    otz = tz.localize(datetime.now())
    return (otz.hour * 3600) + (otz.minute * 60) + otz.second
