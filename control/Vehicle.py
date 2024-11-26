"""
Vehicle.py:
Holds all data regarding the vehicles state. Including, most recent packet received,
calculated values, errors and warnings detected. And provides an
interface for other threads to read and set these values
"""
import threading
import control.config as config

class Vehicle:

    def __init__(self):
        self.lock = threading.Lock()
        self.exit = False  # True when system needs to exit
        self.unchecked = True  # should data be checked for error state

        # packet data received
        self.speed = []                # 0  : Int 0-255: mph 0-32
        self.throttle = []             # 1  : Int 0-255
        self.brake = []                # 2  : Int 0-255
        self.emergency_brake = []      # 3  : Int 0-255
        self.gear = []                 # 4  : Int (0-31:Reverse)
        # (32-64:Neutral) (65-97:Low) (98-130:Mid) (131-163:High) (164-196:Overdrive) (197-255:Unassigned)
        self.steering_angle = []       # 5  : Int Center:127
        self.direction = []            # 6  : Int 0-255 East is zero:Clockwise to 255
        self.battery_voltage = []      # 7  : Int 0-255
        self.battery_current = []      # 8  : Int 0-255
        self.battery_temperature = []  # 9  : Int 0-255
        self.front_L_wheel_speed = []  # 10 : Int 0-255
        self.front_R_wheel_speed = []  # 11 : Int 0-255
        self.distance_to_object = []   # 12 : Int 0-255

        # packet data to send
        self.speedToSend = 0                 # 3  : Int 0-255: mph 0-32
        self.throttleToSend = 0              # 4  : Int 0-255
        self.brakeToSend = 0                 # 5  : Int 0-255
        self.emergency_brakeToSend = 0       # 6  : Int 0-255
        self.gearToSend = 1                  # 7  : Int (0-31:Reverse) (32-64:Neutral) (65-97:Low) (98-130:Mid)
        # (131-163:High) (164-196:Overdrive) (197-255:Unassigned)
        self.steering_angleToSend = 127      # 8  : Int Center:127
        self.directionToSend = 0             # 9  : Int 0-255 East is zero:Clockwise to 255
        self.battery_voltageToSend = 0       # 10 : Int 0-255
        self.battery_currentToSend = 0       # 11 : Int 0-255
        self.battery_temperatureToSend = 0   # 12 : Int 0-255
        self.front_L_wheel_speedToSend = 0   # 13 : Int 0-255
        self.front_R_wheel_speedToSend = 0   # 14 : Int 0-255
        self.distance_to_objectToSend = 0    # 15 : Int 0-255

        # controller information
        self.controllerConnected = False
        self.controllerName = None
        self.controllerReference = None

        # Error states
        self.warning_state = False
        self.critical_error_state = False
        self.radio_state = 0
        self.collision_state = False
        self.battery_depletion = False
        self.battery_overheat = False
        self.excessive_load = False
        self.hill_detection = False
        self.slip_detection = False
        self.hard_turn = False

    # called by, Sender, control-unit, and display
    # used to get data
    def __copy__(self):
        out = Vehicle()
        with self.lock:
            out.exit = self.exit

            # incoming packet data
            out.speed = self.speed.copy()
            out.throttle = self.throttle.copy()
            out.brake = self.brake.copy()
            out.emergency_brake = self.emergency_brake.copy()
            out.gear = self.gear.copy()
            out.steering_angle = self.steering_angle.copy()
            out.direction = self.direction.copy()
            out.battery_voltage = self.battery_voltage.copy()
            out.battery_current = self.battery_current.copy()
            out.battery_temperature = self.battery_temperature.copy()
            out.front_L_wheel_speed = self.front_L_wheel_speed.copy()
            out.front_R_wheel_speed = self.front_R_wheel_speed.copy()
            out.distance_to_object = self.distance_to_object.copy()

            # outgoing command data
            out.speedToSend = self.speedToSend
            out.throttleToSend = self.throttleToSend
            out.brakeToSend = self.brakeToSend
            out.emergency_brakeToSend = self.emergency_brakeToSend
            out.gearToSend = self.gearToSend
            out.steering_angleToSend = self.steering_angleToSend
            out.directionToSend = self.directionToSend
            out.battery_voltageToSend = self.battery_voltageToSend
            out.battery_currentToSend = self.battery_currentToSend
            out.battery_temperatureToSend = self.battery_temperatureToSend
            out.front_L_wheel_speedToSend = self.front_L_wheel_speedToSend
            out.front_R_wheel_speedToSend = self.front_R_wheel_speedToSend
            out.distance_to_objectToSend = self.distance_to_objectToSend

            # Error stats
            out.warning_state = self.warning_state
            out.critical_error_state = self.critical_error_state
            out.collision_state = self.collision_state
            out.battery_depletion = self.battery_depletion
            out.battery_overheat = self.battery_overheat
            out.excessive_load = self.excessive_load
            out.hill_detection = self.hill_detection
            out.slip_detection = self.slip_detection
            out.radio_state = self.radio_state

        return out

    # called by packetReceiver
    # updates fields directly from new packet
    def update_with_packet(self, attributes):
        with self.lock:
            # if PACKET_COUNT reached, remove the oldest packet
            if len(self.speed) == config.PACKET_COUNT:
                self.speed.pop(0)
                self.throttle.pop(0)
                self.brake.pop(0)
                self.emergency_brake.pop(0)
                self.gear.pop(0)
                self.steering_angle.pop(0)
                self.direction.pop(0)
                self.battery_voltage.pop(0)
                self.battery_current.pop(0)
                self.battery_temperature.pop(0)
                self.front_L_wheel_speed.pop(0)
                self.front_R_wheel_speed.pop(0)
                self.distance_to_object.pop(0)

            # append new values to end of list
            self.speed.append(attributes[0])
            self.throttle.append(attributes[1])
            self.brake.append(attributes[2])
            self.emergency_brake.append(attributes[3])
            self.gear.append(attributes[4])
            self.steering_angle.append(attributes[5])
            self.direction.append(attributes[6])
            self.battery_voltage.append(attributes[7])
            self.battery_current.append(attributes[8])
            self.battery_temperature.append(attributes[9])
            self.front_L_wheel_speed.append(attributes[10])
            self.front_R_wheel_speed.append(attributes[11])
            self.distance_to_object.append(attributes[12])
