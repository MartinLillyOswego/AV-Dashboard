from Receiver import Receiver
from Vehicle import Vehicle
from Sender import Sender
import config
import time

# create instance of Vehicle class
vehicle_data = Vehicle()

# start the receiver thread
r = Receiver(vehicle=vehicle_data)
r.start()

# start the sender thread
s = Sender(vehicle=vehicle_data, receiver=r, control_unit=None)
s.start()