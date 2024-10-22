import serial
import serial.tools.list_ports
import threading
import struct
import socket
import time 
import config
from Vehicle import vehicle

class Receiver(threading.Thread):
    def __init__(self, vehicle):
        super(Receiver, self).__init__()
        self.vehicle = vehicle
        self.serial_port = None 
        self.serialconnect()

    def serialconnect(self):
        failed_attempts = 0
        while True:
            ports = serial.tools.list_ports.comports()
            portlist = []

            for onePort in ports: 
                portlist.append(str(onePort))
                print(str(onePort))

            p = input("Select Port: COM")
            selectedport = None

            for x in range(len(portlist)):
                if portlist[x].startswith("COM" + str(p)):
                    selectedport = "COM" + str(p)
                    print(portlist[x])
                    break

            if selectedport:
                try:
                    self.serial_port = serial.Serial(selectedport, baudrate=9600, timeout=1)
                    if not self.serial_port.is_open:
                        self.serial_port.open()
                    print(f"Receiver: Serial port connected")
                    break
                except serial.SerialException:
                    print("Receiver: Failed to connect to serial port")
                    failed_attempts += 1
                    time.sleep(config.SEND_INTERVAL)
            else:
                print("Invalid Port")

    def carlaconnect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.carla_ip, int(self.carla_port)))
            print(f"Receiver: Connected to CARLA")
        except Exception as e:
            print(f"Receiver: Failed to connect to CARLA: {e}")

    def parsetelemetry(self, packet):
        if len(packet) != 60:
            print("Invalid packet")
            return None
        
        rawdata = struct.unpack('f' * 14, packet
        attributes = [
            int(rawdata[0]),  # sender_id
            int(rawdata[1]),  # receiver_id
            rawdata[2],       # error_code
            rawdata[3],       # speed
            rawdata[4],       # throttle
            rawdata[5],       # front_brake
            rawdata[6],       # emergency_brake
            rawdata[7],       # steering_angle
            rawdata[8],       # compass_direction
            rawdata[9],       # Speed Control
            rawdata[10],      # battery_voltage
            rawdata[11],      # battery_current
            rawdata[12],      # battery_temperature
            rawdata[13],      # Front Left Wheel Speed
            rawdata[14],      # Front Left Wheel Speed
            rawdata[15],      # distance_to_object
        ]

        return attributes
    
    def run(self):
        while True:
            if self.serial_port and self.serial_port.in_waiting:
                packet = self.serial_port.read(60)
                data = self.parsetelemetry(packet)
                if data:
                    self.vehicle.update_with_packet(data)
            time.sleep(0.01)
