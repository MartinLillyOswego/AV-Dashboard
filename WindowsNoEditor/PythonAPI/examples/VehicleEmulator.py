"""
Starts the carla simulation which records simulated sensor data
in into an instance of Vehicle.This data is read by the Sender thread
and is packaged and sent to the dashboard over an emulated serial port.

To run, follow the directions given in carla_test.py,
Requires: python v3.7, "pip install carla==0.9.5", carla simulator 9.8, serial port emulator
"""
from CarlaVehicle import CarlaVehicle
from Receiver import Receiver
from Vehicle import Vehicle
from Sender import Sender
import threading
import config
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
cv = CarlaVehicle(outgoing_vehicle=carla_vehicle_data, incoming_vehicle=received_vehicle_commands)
cv.start()

# exit
time.sleep(config.CARLA_SIM_DURATION+10)
print(f"{config.get_time()}: Simulation exiting . . .")
carla_vehicle_data.exit = True
received_vehicle_commands.exit = True