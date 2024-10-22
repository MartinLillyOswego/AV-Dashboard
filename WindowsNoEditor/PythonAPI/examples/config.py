"""
Note: this is the config for VehicleEmulator.py, not the main config / tuning menu,
all values such as 'MY_ID' are from the perspective the vehicle, not the dashboard
"""
from datetime import datetime
import time
import pytz

# Serial connection
USE_CARLA_DATA = True  # True-->Connects to Carla simulation, False-->Connects to Vehicle's radio
CARLA_SERIAL_PORT = 'COM1'  # local emulated serial port
VEHICLE_PORT = 'NA'  # radio's serial port

# Packet info
SEND_INTERVAL = .25  # total wait time elapsed between sending packets
PACKET_COUNT = 60  # number of packets the Vehicle class will store at any given time
MY_ID = 0  # define the Sender ID to be the final string of digits of the sending machine’s IP address
EXTERNAL_ID = 1  # define the Receiver ID to be the final string of digits in the receiving machine’s IP address
PACKET_SIZE = 136  # 17 floats in each half = 2(17*4) = 136 bytes

CARLA_SIM_DURATION = 30  # number of seconds that the carla simulation will run for

# get time for printing only
def get_time():
    tz = pytz.timezone('America/New_York')
    otz = tz.localize(datetime.now())
    return (otz.hour * 3600) + (otz.minute * 60) + otz.second