import time
import threading
from Vehicle import Vehicle


class Shutdown(threading.Thread):
    def __init__(self, vehicle):
        super(Communication, self).__init__()
        self.vehicle = vehicle
    
    def run(self):
        while True:
            if !self.vehicle.unchecked:
                continue
            check_for_error_state()
    
    def check_for_error_state():
        """Appends error codes based on current vehicle state"""
        # High battery temperature
        self.vehicle.battery_overheat = self.vehicle.battery_temperate[-1] > 75
        # Slippery surface
        self.vehicle.slip_detection =  (self.vehicle.throttle[-1] > 0 and self.vehicle.velocity[-1] <= self.vehicle.velocity[-2]) or (self.vehicle.braking_force[-1] > 70 and self.vehicle.velocity[-1] >= self.vehicle.velocity[-2])
        # Low battery voltage
        self.vehicle.battery_depletion = self.vehicle.battery_voltage[-1] < 20
        # High speed with large steering angle
        self.vehicle.hard_turn = abs(self.vehicle.steering_angle[-1]) > 30 and Vehicle.vehicle.velocity[-1] > 60
        # Critically low distance to object
        self.vehicle.collision_state = self.vehicle.distance_to_object[-1] < 20
        # Significant difference in wheel speeds
        # self.vehicle.mismatched_wheel_speed = abs(self.vehicle.fl_wheel_speed[-1] - self.vehicle.fr_wheel_speed[-1]) > 5