"""
Sender.py:
Constructs a new packet after requesting the control unit to generate new commands.
The commands are then packaged according to the AV/RCPv1 protocol and sent over a
serial port to either the CP210radio or the CARLA simulation. These packets are sent
throughout the entire runtime of the dashboard as long as the radio is connected,
otherwise it will reconnect.
"""

from datetime import datetime
from threading import Thread
import numpy as np
import threading
import serial
import config
import struct
import time
import pytz

class Sender(threading.Thread):

    def __init__(self, vehicle, receiver, control_unit, *args, **kwargs):
        super(Sender, self).__init__(*args, **kwargs)
        self.vehicle = vehicle
        self.control_unit = control_unit
        self.receiver = receiver

    # build the packet
    def package_data(self):

        #TODO:
        # pull new commands from control_unit
        # new_commands = self.control_unit.get_vehicle_commands()
        new_commands = None

        # pull last_packet from vehicle class
        vehicle_snapshot = self.vehicle.__copy__()
        ind = len(vehicle_snapshot.velocity) - 1
        if ind == -1:
            return None
        last_packet = [vehicle_snapshot.receiver_id,
                       vehicle_snapshot.sender_id,
                       vehicle_snapshot.error_code[ind],
                       vehicle_snapshot.velocity[ind],
                       vehicle_snapshot.throttle[ind],
                       vehicle_snapshot.braking_force[ind],
                       vehicle_snapshot.hand_brake[ind],
                       vehicle_snapshot.steering_angle[ind],
                       vehicle_snapshot.direction[ind],
                       vehicle_snapshot.gear[ind],
                       vehicle_snapshot.battery_voltage[ind],
                       vehicle_snapshot.battery_current[ind],
                       vehicle_snapshot.battery_temperate[ind],
                       vehicle_snapshot.fl_wheel_speed[ind],
                       vehicle_snapshot.fr_wheel_speed[ind],
                       vehicle_snapshot.distance_to_object[ind],
                       vehicle_snapshot.time[ind]]
        print(f"{config.get_time()}:SendingThread: Packaged: {last_packet}]")


        # populate first half of packet with new commands
        packet_first_half = b""
        if new_commands is not None:
            for float_val in new_commands:
                packet_first_half += bytes(bytearray(struct.pack("f", float_val)))

        # populate last half of packet with last received packet
        packet_last_half = b""
        if last_packet is not None:
            for float_val in last_packet:
                packet_last_half += bytes(bytearray(struct.pack("f", float_val)))

        if packet_first_half == b"":
            packet_first_half = packet_last_half
        return packet_first_half + packet_last_half

    # attempts to send the packet
    @staticmethod
    def send(connection, data):
        if (data is None) or (connection is None):
            return False
        try:
            connection.write(data)
            print(f"{config.get_time()}:SendingThread: Sent: {data}")
        except serial.SerialTimeoutException:
            print(f"{config.get_time()}:SendingThread: Failed to send packet, bad serial connection")
            return False
        return True

    # main loop
    def run(self):
        print(f"{config.get_time()}:SendingThread: Started")
        connection = self.receiver.serial_port
        while True:
            starting_time = time.time()
            if not Sender.send(connection, self.package_data()):
                connection = self.receiver.serial_port
            time.sleep(config.SEND_INTERVAL-(time.time()-starting_time))
            if self.vehicle.exit:
                break