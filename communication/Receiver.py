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
            if config.USE_CARLA_DATA:
                serial_id = config.CARLA_SERIAL_PORT
            try:
                self.serial_port = serial.Serial(serial_id, baudrate=9600, timeout=1)
                if not self.serial_port.is_open:
                    self.serial_port.open()
                print(f"{config.get_time()}:Receiver: Serial port connected")
                break
            except serial.SerialException as e:
                print(f"{config.get_time()}:Receiver: Failed to connect to serial port {e}")
                time.sleep(config.SEND_INTERVAL)

    @staticmethod
    def parse_telemetry(packet):
        if len(packet) != config.PACKET_SIZE:
            print("Invalid packet")
            return None
        parsedPac = np.frombuffer(packet, np.float32)
        # don't record the packets that we ourselves sent
        if parsedPac[0] == config.MY_ID:
            return None
        out = []
        for da in parsedPac:
            out.append(float(f"{da:.3f}"))
        return out

    # main loop
    def run(self):
        print(f"{config.get_time()}:Receiver: Started")
        self.serial_connect()
        while True:
            if self.serial_port and self.serial_port.in_waiting:
                packet = self.serial_port.read(config.PACKET_SIZE)
                data = self.parse_telemetry(packet)
                if data is not None:
                    #print(f"{config.get_time()}:Receiver: got: {data}")
                    self.vehicle.update_with_packet(data)
            time.sleep(0.01)
            if self.vehicle.exit:
                break
