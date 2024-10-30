import time
from threading import Thread
from Vehicle import Vehicle
import threading
import config

#TODO:
# implement input devices class
# from inputDevice import inputDevice

class ControlUnit(threading.Thread):

    def __init__(self, vehicle, *args, **kwargs):
        super(ControlUnit, self).__init__(*args, **kwargs)
        self.vehicle = vehicle


    # constructs data to be displayed
    def generate_display_data(self):
        #TODO:
        # generate all required values and assets neeed to fully update the display
        # display_data + self.generate_vehicle_error() + otherStuff
        self.vehicle.update_calculated_data(display_data)

    # called when generating response commands, responsible for observing vehicle errors
    def generate_vehicle_error(self):
        #TODO:
        # reads vehicle state to determine if it has entered a error / warning state
        vehicle_state = self.vehicle.__copy__()
        return errors

    # determinces any necessary commands to maintain vehicle safety
    def generate_responce_commands(self):
        #TODO:
        # read errors and vehicle state to determine any necessary responce commands
        pass

    # constructs a new set of outgoing vehicle commands
    def generate_vehicle_commands(self):
        #TODO:
        # build final output of commands with a collection of input devices
        # new_commands = self.controller_commands + self.keyboard_commands + self.response_commands
        pass

    # called by sender to send new commands
    def get_vehicle_commands(self):
        return

    # main loop, update command and display fields
    def run(self):
        while True:
            st = time.time()
            self.generate_vehicle_commands()
            self.generate_display_data()
            time.sleep(config.CONTROL_UNIT_INTERVAL-(time.time()-st))
