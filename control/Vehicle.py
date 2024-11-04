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
        self.exit = False

        # packet data
        self.sender_id = 0
        self.receiver_id = 1
        self.velocity = []
        self.steering_angle = []
        self.throttle = []
        self.braking_force = []
        self.hand_brake = []
        self.battery_voltage = []
        self.battery_current = []
        self.battery_temperate = []
        self.distance_to_object = []
        self.direction = []
        self.time = []
        self.error_code = []
        self.gear = []
        self.fl_wheel_speed = []
        self.fr_wheel_speed = []

        # add more packet fields as needed

        # display data
        self.display_velocity = []
        self.acceleration = []
        self.display_battery_temperate = []
        self.display_battery_voltage = []
        self.display_battery_current = []
        self.display_steering_angle = -1
        self.display_direction = -1
        self.position_graphic = -1
        self.total_distance_traveled = -1
        self.display_throttle = []
        self.display_slip_angle = []
        self.display_distance_to_object = -1
        self.display_error_code = -1
        # add more display fields as needed

    # called by, Sender, control-unit, and display
    # used to get data
    def __copy__(self):
        out = Vehicle()
        with self.lock:
            out.exit = self.exit
            out.sender_id = self.sender_id
            out.receiver_id = self.receiver_id
            out.velocity = self.velocity.copy()
            out.steering_angle = self.steering_angle.copy()
            out.throttle = self.throttle.copy()
            out.braking_force = self.braking_force.copy()
            out.hand_brake = self.hand_brake.copy()
            out.battery_voltage = self.battery_voltage.copy()
            out.battery_current = self.battery_current.copy()
            out.battery_temperate = self.battery_temperate.copy()
            out.distance_to_object = self.distance_to_object.copy()
            out.direction = self.direction.copy()
            out.time = self.time.copy()
            out.error_code = self.error_code.copy()
            out.display_velocity = self.display_velocity.copy()
            out.acceleration = self.acceleration.copy()
            out.display_battery_temperate = self.display_battery_temperate.copy()
            out.display_battery_voltage = self.display_battery_voltage.copy()
            out.display_battery_current = self.display_battery_current.copy()
            out.display_steering_angle = self.display_steering_angle
            out.display_direction = self.display_direction
            out.position_graphic = self.position_graphic
            out.total_distance_traveled = self.total_distance_traveled
            out.display_throttle = self.display_throttle.copy()
            out.display_slip_angle = self.display_slip_angle.copy()
            out.display_distance_to_object = self.display_distance_to_object
            out.display_error_code = self.display_error_code
            out.gear = self.gear.copy()
            out.fl_wheel_speed = self.fl_wheel_speed.copy()
            out.fr_wheel_speed = self.fr_wheel_speed.copy()
        return out

    # called by packetReceiver,
    # updates fields directly from new packet
    def update_with_packet(self, attributes):
        with self.lock:
            self.sender_id = attributes[1]
            self.receiver_id = attributes[0]

            # if PACKET_COUNT reached, remove the oldest packet
            if len(self.velocity) == config.PACKET_COUNT:
                self.velocity.pop(0)
                self.steering_angle.pop(0)
                self.throttle.pop(0)
                self.braking_force.pop(0)
                self.hand_brake.pop(0)
                self.battery_voltage.pop(0)
                self.battery_current.pop(0)
                self.battery_temperate.pop(0)
                self.distance_to_object.pop(0)
                self.direction.pop(0)
                self.time.pop(0)
                self.error_code.pop(0)
                self.gear.pop(0)
                self.fl_wheel_speed.pop(0)
                self.fr_wheel_speed.pop(0)

            self.error_code.append(attributes[2])
            self.velocity.append(attributes[3])
            self.throttle.append(attributes[4])
            self.braking_force.append(attributes[5])
            self.hand_brake.append(attributes[6])
            self.steering_angle.append(attributes[7])
            self.direction.append(attributes[8])
            self.gear.append(attributes[9])
            self.battery_voltage.append(attributes[10])
            self.battery_current.append(attributes[11])
            self.battery_temperate.append(attributes[12])
            self.fl_wheel_speed.append(attributes[13])
            self.fr_wheel_speed.append(attributes[14])
            self.distance_to_object.append(attributes[15])
            self.time.append(attributes[16])

    # called by controlUnit,
    # update fields not directly given by the packet
    def update_calculated_data(self, attributes):
        with self.lock:
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

