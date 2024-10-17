import threading
import serial
import config
import time

PORT = 'COM2'

class SM(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(SM, self).__init__(*args, **kwargs)
        self.port = -1

    def recv(self, raw=0):
        if self.port == -1:
            return
        if self.port.in_waiting:
            if raw:
                return self.port.read(config.PACKET_SIZE)
            else:
                return self.port.read(config.PACKET_SIZE)

    def run(self):
        print(f"{config.get_time()}:SM: Started")
        time.sleep(3)
        self.port = serial.Serial(PORT)
        while True:
            packet = self.recv()
            if str(packet) != "None":
                print(f"{config.get_time()}:SM:{packet}")