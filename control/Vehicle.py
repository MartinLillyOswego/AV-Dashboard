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

        # packet data received
        self.speed = []  # 4  : Int 0-255: mph 0-32
        self.throttle = []  # 5  : Int 0-255
        self.brake = []  # 6  : Int 0-255
        self.emergency_brake = []  # 8  : Int 0-255
        self.gear = []  # 9  : Int (0-31:Reverse) (32-64:Neutral) (65-97:Low) (98-130:Mid) (131-163:High) (164-196:Overdrive) (197-255:Unassigned)
        self.steering_angle = []  # 10 : Int Center:127
        self.direction = []  # 11 : Int 0-255 East is zero:Clockwise to 255
        self.battery_voltage = []  # 11 : Int 0-255
        self.battery_current = []  # 12 : Int 0-255
        self.battery_temperature = []  # 13 : Int 0-255
        self.front_L_wheel_speed = []  # 14 : Int 0-255
        self.front_R_wheel_speed = []  # 15 : Int 0-255
        self.distance_to_object = []  # 16 : Int 0-255

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

    # called by, Sender, control-unit, and display
    # used to get data
    def __copy__(self):
        out = Vehicle()
        with self.lock:
            out.exit = self.exit

            # Packet data
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

    # update fields not directly given by the packet
    def update_calculated_data(self, attributes):
        with self.lock:
            '''
            self.display_velocity = attributes[0].copy()
            self.acceleration = attributes[1].copy()
            self.display_battery_temperate = attributes[2].copy()
            self.display_battery_voltage = attributes[3].copy()
            self.display_battery_current = attributes[4].copy()
            self.display_steering_angle = attributes[5]
            self.display_direction = attributes[6]
            self.position_graphic = attributes[7].copy()  # data type of this field is tbd
            self.total_distance_traveled = attributes[8]
            self.display_throttle = attributes[9].copy()
            self.display_slip_angle = attributes[10].copy()
            self.display_distance_to_object = attributes[11]
            self.display_error_code = attributes[12]
            '''