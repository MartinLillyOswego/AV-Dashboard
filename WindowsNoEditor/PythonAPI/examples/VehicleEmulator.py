"""
Starts the carla simulation which records simulated sensor data
in into an instance of Vehicle.This data is read by the Sender thread
and is packaged and sent to the dashboard over an emulated serial port.

To run, follow the directions given in carla_test.py,
Requires: python v3.7, "pip install carla==0.9.5", carla simulator 9.8, serial port emulator

NOTE: the file "manual_control.py" originates form your instillation of Carla but has been
modified to write data to an instance of the Vehicle class. This version provided will only work with
Carla v0.9.8, to run with newer Carla versions, modified your instance of "manual_control.py" provided
with your installation of Carla, and apply the same changes as seen in this version of "manual_control.py"
"""
from manual_control_v0_9_8 import CarlaThread
from emulator_Receiver import Receiver
from emulator_Vehicle import Vehicle
from emulator_Sender import Sender
import threading
import time

# create shared instances of Vehicle class
carla_vehicle_data = Vehicle()
received_vehicle_commands = Vehicle()

# start the vehicle emulator's receive thread
r = Receiver(vehicle=received_vehicle_commands)
r.start()

# start the vehicle emulator's send thread
s = Sender(vehicle=carla_vehicle_data, receiver=r, control_unit=None)
s.start()

# start the carla thread, which updates a shared instance of Vehicle
ct = CarlaThread(outgoing_vehicle=carla_vehicle_data, incoming_vehicle=received_vehicle_commands)
ct.start()