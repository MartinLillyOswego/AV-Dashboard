"""
Vehicle.py:
Holds all data regarding the vehicles state. Including, most recent packet received,
calculated values, errors and warnings detected. And provides an
interface for other threads to read and set these values
"""
import threading
import config as config

class Vehicle:

    def __init__(self):
        self.lock = threading.Lock()
        self.exit = False  # True when system needs to exit
        self.unchecked = True # should data be checked for error state

        # packet data received
        self.throttle            = []  # 1  : Int 0-255
        self.brake               = []  # 2  : Int 0-255
        self.emergency_brake     = []  # 3  : Int 0-255
        self.gear                = []  # 4  : Int (0-31:Reverse) (32-64:Neutral) (65-97:Low) (98-130:Mid) (131-163:High) (164-196:Overdrive) (197-255:Unassigned)
        self.steering_angle      = []  # 5  : Int Center:127

        # packet data to send
        self.speedToSend               = [0]   # 3  : Int 0-255: mph 0-32
        self.throttleToSend            = [0]   # 4  : Int 0-255
        self.brakeToSend               = [0]   # 5  : Int 0-255
        self.emergency_brakeToSend     = [0]   # 6  : Int 0-255
        self.gearToSend                = [1]   # 7  : Int (0-31:Reverse) (32-64:Neutral) (65-97:Low) (98-130:Mid) (131-163:High) (164-196:Overdrive) (197-255:Unassigned)
        self.steering_angleToSend      = [127] # 8  : Int Center:127
        self.directionToSend           = [0]   # 9  : Int 0-255 East is zero:Clockwise to 255
        self.battery_voltageToSend     = [0]   # 10 : Int 0-255
        self.battery_currentToSend     = [0]   # 11 : Int 0-255
        self.battery_temperatureToSend = [0]   # 12 : Int 0-255
        self.front_L_wheel_speedToSend = [0]   # 13 : Int 0-255
        self.front_R_wheel_speedToSend = [0]   # 14 : Int 0-255
        self.distance_to_objectToSend  = [0]   # 15 : Int 0-255

    # called by, Sender, control-unit, and display
    # used to get data
    def __copy__(self):
        out = Vehicle()
        with self.lock:
            out.exit = self.exit

            # Packet data
            out.speed = self.speedToSend.copy()
            out.throttle = self.throttleToSend.copy()
            out.brake = self.brakeToSend.copy()
            out.emergency_brake = self.emergency_brakeToSend.copy()
            out.gear = self.gearToSend.copy()
            out.steering_angle = self.steering_angleToSend.copy()
            out.direction = self.directionToSend.copy()
            out.battery_voltage = self.battery_voltageToSend.copy()
            out.battery_current = self.battery_currentToSend.copy()
            out.battery_temperature = self.battery_temperatureToSend.copy()
            out.front_L_wheel_speed = self.front_L_wheel_speedToSend.copy()
            out.front_R_wheel_speed = self.front_R_wheel_speedToSend.copy()
            out.distance_to_object = self.distance_to_objectToSend.copy()

        return out

    # called by packetReceiver
    # updates fields directly from new packet
    def update_with_packet(self, attributes):
        with self.lock:
            # if PACKET_COUNT reached, remove the oldest packet
            if len(self.throttle) == config.PACKET_COUNT:
                self.throttle.pop(0)
                self.brake.pop(0)
                self.emergency_brake.pop(0)
                self.gear.pop(0)
                self.steering_angle.pop(0)

            # append new values to end of list
            self.throttle.append(attributes[0])
            self.brake.append(attributes[1])
            self.emergency_brake.append(attributes[2])
            self.gear.append(attributes[3])
            self.steering_angle.append(attributes[4])

    # updates from carla
    def update_with_packet_from_carla(self, attributes):
        with self.lock:
            # if PACKET_COUNT reached, remove the oldest packet
            if len(self.speedToSend) == config.PACKET_COUNT:
                self.speedToSend.pop(0)
                self.throttleToSend.pop(0)
                self.brakeToSend.pop(0)
                self.emergency_brakeToSend.pop(0)
                self.gearToSend.pop(0)
                self.steering_angleToSend.pop(0)
                self.directionToSend.pop(0)
                self.battery_voltageToSend.pop(0)
                self.battery_currentToSend.pop(0)
                self.battery_temperatureToSend.pop(0)
                self.front_L_wheel_speedToSend.pop(0)
                self.front_R_wheel_speedToSend.pop(0)
                self.distance_to_objectToSend.pop(0)

            # append new values to end of list
            self.speedToSend.append(attributes[0])
            self.throttleToSend.append(attributes[1])
            self.brakeToSend.append(attributes[2])
            self.emergency_brakeToSend.append(attributes[3])
            self.gearToSend.append(attributes[4])
            self.steering_angleToSend.append(attributes[5])
            self.directionToSend.append(attributes[6])
            self.battery_voltageToSend.append(attributes[7])
            self.battery_currentToSend.append(attributes[8])
            self.battery_temperatureToSend.append(attributes[9])
            self.front_L_wheel_speedToSend.append(attributes[10])
            self.front_R_wheel_speedToSend.append(attributes[11])
            self.distance_to_objectToSend.append(attributes[12])


