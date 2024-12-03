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
            self.battery_depletion = self.battery_voltage[-1] < config.BATTERY_LOW_THRESHOLD
            self.battery_overheat = self.battery_temperature[-1] > config.BATTERY_OVERHEAT_THRESHOLD
            self.collision_state = self.distance_to_object[-1] < config.COLLISION_THRESHOLD
            self.hard_turn = abs(self.steering_angle[-1] - 127) > config.HARD_TURN_THRESHOLD
            self.excessive_load = self.battery_current[-1] > config.EXCESSIVE_LOAD_THRESHOLD
            self.hill_detection = (
                self.throttle[-1] > config.HILL_DETECTION_THROTTLE
                and self.speed[-1] < config.HILL_DETECTION_SPEED
            )
            self.slip_detection = abs(
                self.front_L_wheel_speed[-1] - self.front_R_wheel_speed[-1]
            ) > config.SLIP_DETECTION_THRESHOLD


            self.warning_state = (
                self.battery_depletion
                or self.battery_overheat
                or self.hard_turn
                or self.slip_detection
            )


            self.critical_error_state = (
                self.collision_state
                or self.battery_overheat
                or self.excessive_load
            )