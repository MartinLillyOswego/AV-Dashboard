from control.Vehicle import Vehicle
import serial.tools.list_ports
import control.config as config
import numpy as np
import threading
import serial
import struct
import time


class Receiver(threading.Thread):

    def __init__(self, vehicle):
        super(Receiver, self).__init__()
        self.vehicle = vehicle
        self.serial_port = None

    def serial_connect(self):
        while True:
            serial_id = config.VEHICLE_PORT
            try:
                self.serial_port = serial.Serial(serial_id, baudrate=9600, timeout=1)
                if not self.serial_port.is_open:
                    self.serial_port.open()
                print(f"{config.get_time()}:Receiver: Serial port connected")
                break
            except serial.SerialException as e:
                print(f"{config.get_time()}:Receiver: Failed to connect to serial port {e}")
                time.sleep(config.SEND_INTERVAL)

    # main loop
    def run(self):
        print(f"{config.get_time()}:Receiver: Started")
        self.serial_connect()
        while True:
            if self.serial_port and self.serial_port.in_waiting:
                packet = self.serial_port.read(config.PACKET_SIZE)
                
                '''
                error checking function?
                if len(packet) != config.PACKET_SIZE:
                print("Invalid packet")
                return None
                
                '''
                self.vehicle.update_with_packet(packet)
            #time.sleep(config.SEND_INTERVAL)
            if self.vehicle.exit:
                break