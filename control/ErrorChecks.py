import time
import threading
from control.Vehicle import Vehicle


class ErrorChecks(threading.Thread):
    def __init__(self, vehicle):
        super(Communication, self).__init__()
        self.vehicle = vehicle
    
    def run(self):
        while True:
            if not self.vehicle.unchecked:
                continue
            check_for_error_state()
            self.vehicle.unchecked = False
    
    def check_for_error_state():
        with self.lock:
            self.vehicle.battery_depletion = self.vehicle.battery_voltage[-1] < config.BATTERY_LOW_THRESHOLD
            self.vehicle.battery_overheat = self.vehicle.battery_temperature[-1] > config.BATTERY_OVERHEAT_THRESHOLD
            self.vehicle.collision_state = self.vehicle.distance_to_object[-1] < config.COLLISION_THRESHOLD
            self.vehicle.hard_turn = abs(self.vehicle.steering_angle[-1] - 127) > config.HARD_TURN_THRESHOLD
            self.vehicle.excessive_load = self.vehicle.battery_current[-1] > config.EXCESSIVE_LOAD_THRESHOLD
            self.vehicle.hill_detection = (
                self.vehicle.throttle[-1] > config.HILL_DETECTION_THROTTLE
                and self.vehicle.speed[-1] < config.HILL_DETECTION_SPEED
            )
            self.vehicle.slip_detection = abs(
                self.vehicle.front_L_wheel_speed[-1] - self.vehicle.front_R_wheel_speed[-1]
            ) > config.SLIP_DETECTION_THRESHOLD


            self.vehicle.warning_state = (
                self.vehicle.battery_depletion
                or self.vehicle.battery_overheat
                or self.vehicle.hard_turn
                or self.vehicle.slip_detection
            )


            self.vehicle.critical_error_state = (
                self.vehicle.collision_state
                or self.vehicle.battery_overheat
                or self.vehicle.excessive_load
            )