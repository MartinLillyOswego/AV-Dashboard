"""
Reads and writes from config.txt, values can be updated manually in that file or in the tuning menu
"""
from datetime import datetime
import time
import pytz
import re

# known values
CONFIG_FILE = "control/config.txt"
USE_CARLA_DATA = True  # True-->Connects to Carla simulation, False-->Connects to Vehicle's radio
CONTROL_UNIT_INTERVAL = 0.2
CARLA_SIM_DURATION = 30  # number of seconds that the carla simulation will run for

# values to be loaded from file
VEHICLE_PORT = -1  # radio's serial port
SEND_INTERVAL = -1  # total wait time elapsed between sending packets
PACKET_COUNT = -1  # number of packets the Vehicle class will store at any given time
MY_ID = -1  # define the Sender ID to be the final string of digits of the sending machine’s IP address
EXTERNAL_ID = -1  # define the Receiver ID to be the final string of digits in the receiving machine’s IP address
PACKET_SIZE = -1  # 17 floats in each half = 2(17*4) = 136 bytes
MAX_SPEED = -1
CARLA_SERIAL_PORT = -1

# pull values from config.txt
def read():
    try:
        global VEHICLE_PORT, SEND_INTERVAL, PACKET_SIZE, PACKET_COUNT, MY_ID, EXTERNAL_ID, MAX_SPEED, CARLA_SERIAL_PORT
        with open(CONFIG_FILE, 'r') as file:
            lines = file.readlines()
        vals = []
        for line in lines:
            vals.append([exp.group() for exp in re.finditer(r": (.{,16})", str(line))][0][2:])
        VEHICLE_PORT = str(vals[0])
        SEND_INTERVAL = float(vals[1])
        PACKET_COUNT = int(vals[2])
        MY_ID = int(vals[3])
        EXTERNAL_ID = int(vals[4])
        PACKET_SIZE = int(vals[5])
        MAX_SPEED = float(vals[6])
        CARLA_SERIAL_PORT = VEHICLE_PORT  # local emulated serial port
    except:
        raise RuntimeError(f"{get_time()}:Config: Failed to read file")

# put values into config.txt
def write():
    try:
        new_config = f"""VEHICLE_PORT: {VEHICLE_PORT}
SEND_INTERVAL: {SEND_INTERVAL}
PACKET_COUNT: {PACKET_COUNT} 
MY_ID: {MY_ID}
EXTERNAL_ID: {EXTERNAL_ID}
PACKET_SIZE: {PACKET_SIZE}
MAX_SPEED: {MAX_SPEED}"""
        with open(CONFIG_FILE, "w") as file:
            file.write(new_config)
    except:
        raise RuntimeError(f"{get_time()}:Config: Failed to write file")

# get time for printing only
def get_time():
    tz = pytz.timezone('America/New_York')
    otz = tz.localize(datetime.now())
    return (otz.hour * 3600) + (otz.minute * 60) + otz.second
