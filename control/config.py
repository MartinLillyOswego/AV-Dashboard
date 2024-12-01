"""
Reads and writes from config.txt, values can be updated manually in that file or in the tuning menu
"""
from datetime import datetime
import time
import pytz
import re

# known values
CONFIG_FILE = "control/config.txt"
CONFIG_FILE_MC = "control/configMC.txt"

# values to be loaded from file
VEHICLE_PORT = -1  # radio's serial port
LOCAL_PORT = -1  # emulated serial port
USE_LOCAL_PORT = False  # run over an emulated serial port, rather than radio
SEND_INTERVAL = -1  # total wait time elapsed between sending packets
PACKET_COUNT = -1  # number of packets the Vehicle class will store at any given time
MAX_SPEED = -1
PACKET_HEADER = b""
PACKET_SIZE = 16

# pull values from config.txt
def read(input_file):
    try:
        global VEHICLE_PORT, SEND_INTERVAL, PACKET_COUNT, MAX_SPEED, PACKET_HEADER, LOCAL_PORT, USE_LOCAL_PORT,\
            PACKET_SIZE
        with open(input_file, 'r') as file:
            lines = file.readlines()
        vals = []
        for line in lines:
            vals.append([exp.group() for exp in re.finditer(r": (.{,16})", str(line))][0][2:])
        print(vals)
        VEHICLE_PORT = str(vals[0])
        LOCAL_PORT = str(vals[1])

        if str(vals[2]) == "True":
            USE_LOCAL_PORT = True
        else:
            USE_LOCAL_PORT = False

        SEND_INTERVAL = float(vals[3])
        PACKET_COUNT = int(vals[4])
        PACKET_HEADER = str(vals[5])

        # pull packet header
        valsH = [exp.group() for exp in re.finditer(r"[0-9]+", str(PACKET_HEADER))]
        b = b""
        for val in valsH:
            b += int(val).to_bytes(1, "big")
        PACKET_HEADER = b

        MAX_SPEED = float(vals[6])
        PACKET_SIZE = int(vals[7])

    except:
        raise RuntimeError(f"{get_time()}:Config: Failed to read file")

# put values into config.txt
def write():
    try:
        header = PACKET_HEADER
        if type(header) == bytes:
            header = f"{int(header[0])}.{int(header[1])}.{int(header[2])}"
        new_config = f"""RADIO_PORT: {VEHICLE_PORT}
LOCAL_CARLA_PORT: {LOCAL_PORT}
USE_LOCAL_PORT: {USE_LOCAL_PORT}
SEND_INTERVAL: {SEND_INTERVAL}
MAX_PACKET_COUNT: {PACKET_COUNT} 
PACKET_HEADER: {header}
MAX_SPEED: {MAX_SPEED}
INCOMING_PACKET_SIZE: {PACKET_SIZE}
"""
        with open(CONFIG_FILE, "w") as file:
            file.write(new_config)
    except:
        raise RuntimeError(f"{get_time()}:Config: Failed to write file")

# get time for printing only
def get_time():
    tz = pytz.timezone('America/New_York')
    otz = tz.localize(datetime.now())
    return (otz.hour * 3600) + (otz.minute * 60) + otz.second
