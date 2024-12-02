'''
This class gives methods to communicate over Serial. 
'''

# Imports
from control.Vehicle import Vehicle
import serial.tools.list_ports
import control.config as config
import threading
import serial
import time
import os

class Communication(threading.Thread):

    def __init__(self, vehicle):
        super(Communication, self).__init__()
        self.vehicle = vehicle
        self.serial_port = None

    def serial_connect(self):
        # Assign serial id from config file
        serial_id = config.VEHICLE_PORT

        # If using local port for one computer testing
        if config.USE_LOCAL_PORT:
            serial_id = config.LOCAL_PORT

        # Try to connect to serial
        try:
            self.serial_port = serial.Serial(serial_id, baudrate=115200, timeout=1)
            if not self.serial_port.is_open:
                self.serial_port.open()
            print(f"{config.get_time()}:Communication: Serial port connected")
            # Communication flag true
            self.vehicle.serial_connected = True

        except serial.SerialException as e:
            print(f"{config.get_time()}:Communication: Failed to connect to serial port {e}")
            # Communication flag false
            self.vehicle.serial_connected = False
        time.sleep(0.2)

    def package_data(self):
        # pull new values to send from controls
        packet = [self.vehicle.throttleToSend,
                  self.vehicle.brakeToSend,
                  self.vehicle.emergency_brakeToSend,
                  self.vehicle.gearToSend,
                  self.vehicle.steering_angleToSend]

        if not config.USE_LOCAL_PORT:
            out = config.PACKET_HEADER + bytes(packet)

        if True:
            os.system("cls")
            print(f"\033[H\033[J", end="")
            print(f"Throttle  : {self.vehicle.throttleToSend}")
            print(f"Brake     : {self.vehicle.brakeToSend}")
            print(f"Steer     : {self.vehicle.steering_angleToSend}")
            print(f"Gear      : {self.vehicle.gearToSend}")
            print(f"Handbrake : {self.vehicle.emergency_brakeToSend}")
            print(f"Controller: {self.vehicle.controller_name}, Status: {self.vehicle.controller_connected}")
            print(f"Keyboard  : {self.vehicle.keyboard_name}, Status: {self.vehicle.keyboard_connected}")
            print(f"Comm Speed: {self.vehicle.communication_time}")
        return out

    @staticmethod
    def send(connection, data):
        if (data is None) or (connection is None):
            return False
        try:
            connection.write(data)
            #print("sent")
        except serial.SerialTimeoutException:
            #print(f"{config.get_time()}:Communication: Failed to send packet, bad serial connection")
            return False
        return True

    # main loop
    def run(self):
        # connect to serial port
        self.serial_connect()

        # Loop through send and receive while serial is connected
        while self.vehicle.serial_connected:

            # call data package method
            data = self.package_data()

            # Start full communication timer
            initial_time = time.monotonic()

            # if unable to send on serial connection
            if not self.send(self.serial_port, data):
                self.vehicle.sent = False
                self.vehicle.serial_connected = False
            else:
                # packet was sent
                self.vehicle.sent = True

            # Take first timeout reading
            start_timeout = time.monotonic()

            # While nothing on buffer wait for max allowed timeout
            while not self.serial_port.in_waiting:
                # If more than one second has elapsed
                if (time.monotonic() - start_timeout) > 1:
                    #Set vehicle radio state to one
                    self.vehicle.radio_state = 2
                    self.vehicle.received = False
                    self.vehicle.communication_time = 1
                    break
                    # where connection error state is triggered

            # Read data if available
            if self.serial_port.in_waiting:
                # Check time of received
                self.vehicle.communication_time = time.monotonic() - initial_time
                self.vehicle.received = True
                packet = self.serial_port.read(config.PACKET_SIZE)
                # update packet
                self.vehicle.update_with_packet(packet)
                #print (f"{packet}")

            # delay time
            time.sleep(config.SEND_INTERVAL)
