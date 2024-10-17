"""
Starts the carla simulation which records simulated sensor data
in into an instance of Vehicle.This data is read by the Sender thread
and is packaged and sent to the dashboard over an emulated serial port.

To run, follow the directions given in carla_test.py,
Requires: python v3.7, "pip install carla==0.9.5", carla simulator 9.8, serial port emulator
"""

from Vehicle import Vehicle
from Sender import Sender
from SM import SM
import threading
from CarlaVehicle import CarlaVehicle
import time

# create shared instance of Vehicle class
vehicle = Vehicle()

# start the dashboard send thread
t = Sender(vehicle=vehicle, control_unit=None)
t.start()

# start the serial monitor, used for testing only
sm = SM()
sm.start()

# start the carla thread, which updates a shared instance of Vehicle
cv = CarlaVehicle(vehicle=vehicle)
cv.start()