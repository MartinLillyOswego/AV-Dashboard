from Receiver import Receiver
from Vehicle import Vehicle
import config

# create instances of Vehicle class
vehicle_data = Vehicle()

# start the receiver thread
r = Receiver(vehicle=vehicle_data)
r.start()
