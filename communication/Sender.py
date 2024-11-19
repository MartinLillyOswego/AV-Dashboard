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
import control.config as config
import numpy as np
import threading
import serial
import struct
import time
import pytz
from control.Controller import Controller

class Sender(threading.Thread):

    def __init__(self, vehicle, receiver, *args, **kwargs):
        super(Sender, self).__init__(*args, **kwargs)
        self.vehicle = vehicle
        self.receiver = receiver
        self.controller = Controller()

    # build the packet
    def package_data(self):
        # pull last_packet from vehicle class
        vehicle_snapshot = self.vehicle.__copy__()
        ind = len(vehicle_snapshot.speed) - 1
        
        # If no data is available yet
        if ind == -1:
            return None
            
        # Assign initial values to 
        # End of packet/ Last received data
        end_packet = [0,                                     #1  SenderId   : ICP of Vehicle 
                      0,                                     #2  ReceiverID : ICP of Dashboard
                      23,
                      vehicle_snapshot.speed[ind],      
                      vehicle_snapshot.throttle[ind],
                      vehicle_snapshot.brake[ind],
                      vehicle_snapshot.emergency_brake[ind],
                      vehicle_snapshot.gear[ind],
                      vehicle_snapshot.steering_angle[ind],
                      vehicle_snapshot.direction[ind],
                      vehicle_snapshot.battery_voltage[ind],
                      vehicle_snapshot.battery_current[ind],
                      vehicle_snapshot.battery_temperature[ind],
                      vehicle_snapshot.front_L_wheel_speed[ind],
                      vehicle_snapshot.front_R_wheel_speed[ind],
                      vehicle_snapshot.distance_to_object[ind]]

        # Beginning of packet/ Commands to send
        beginning_packet = [0,
                           1,
                           23,
                           vehicle_snapshot.speed[ind],
                           vehicle_snapshot.throttle[ind],
                           vehicle_snapshot.brake[ind],
                           vehicle_snapshot.emergency_brake[ind],
                           vehicle_snapshot.gear[ind],
                           vehicle_snapshot.steering_angle[ind],
                           vehicle_snapshot.direction[ind],
                           vehicle_snapshot.battery_voltage[ind],
                           vehicle_snapshot.battery_current[ind],
                           vehicle_snapshot.battery_temperature[ind],
                           vehicle_snapshot.front_L_wheel_speed[ind],
                           vehicle_snapshot.front_R_wheel_speed[ind],
                           vehicle_snapshot.distance_to_object[ind]]

        # Take new controller commands
        new_commands = self.controller.get_vehicle_commands(beginning_packet)
        
        # Request error confirmation from control unit/ Control Responses to overwrite packet values

        # package byte string
        packetToSend = b''
        packetToSend += bytes(new_commands + end_packet)
        
        # print packet out
        #if ind % 10:
            #print(f"{packetToSend}")
            #print(f"{new_commands}")

        # return completed packet to send out
        return packetToSend


    # attempts to send the packet
    @staticmethod
    def send(connection, data):
        if (data is None) or (connection is None):
            return False
        try:
            print("Sent: " + str(data))
            connection.write(data)
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
            time.sleep(0.2)
            #if config.SEND_INTERVAL-(time.time()-starting_time) > 0:
            #    time.sleep(config.SEND_INTERVAL-(time.time()-starting_time))
            if self.vehicle.exit:
                break
