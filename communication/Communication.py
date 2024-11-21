from control.Vehicle import Vehicle
import serial.tools.list_ports
import control.config as config
import threading
import serial
import time
from control.Controller import Controller


class Communication(threading.Thread):

    def __init__(self, vehicle):
        super(Communication, self).__init__()
        self.vehicle = vehicle
        self.serial_port = None
        self.controller = Controller()

    def serial_connect(self):
        while True:
            serial_id = config.VEHICLE_PORT
            if config.USE_LOCAL_PORT:
                serial_id = config.LOCAL_PORT
            try:
                self.serial_port = serial.Serial(serial_id, baudrate=115200, timeout=1)
                if not self.serial_port.is_open:
                    self.serial_port.open()
                print(f"{config.get_time()}:Communication: Serial port connected")
                self.vehicle.radio_state = 2
                break
            except serial.SerialException as e:
                print(f"{config.get_time()}:Communication: Failed to connect to serial port {e}")
                time.sleep(0.1)

    def package_data(self):
        # pull last_packet from vehicle class
        vehicle_snapshot = self.vehicle.__copy__()
        ind = len(vehicle_snapshot.speed) - 1
        # if no data is available yet (only occurs on program start up)
        if ind == -1:
            packet = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            packet = [vehicle_snapshot.speed[ind],
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
        # pull new commands
        new_commands = self.controller.get_vehicle_commands(packet)
        # send with header when using radios
        out = bytes(new_commands)
        if not config.USE_LOCAL_PORT:
            out = config.PACKET_HEADER + out
        print(f"{config.get_time()}:Sending: {new_commands}")
        print(f"{config.get_time()}:Sending: {out}")
        return out

    @staticmethod
    def send(connection, data):
        if (data is None) or (connection is None):
            return False
        try:
            connection.write(data)
        except serial.SerialTimeoutException:
            print(f"{config.get_time()}:Communication: Failed to send packet, bad serial connection")
            return False
        return True

    # main loop
    def run(self):
        # connect to serial port
        self.serial_connect()
        while True:

            # read Packet
            st = time.monotonic()
            while not self.serial_port.in_waiting:
                if (time.monotonic() - st) > 1:
                    self.vehicle.radio_state = 1
                    break
            if self.serial_port.in_waiting:
                packet = self.serial_port.read(config.PACKET_SIZE)
                print(f"{config.get_time()}:Received: {packet}")
                self.vehicle.update_with_packet(packet)  # update packet

            # call send method
            time.sleep(config.SEND_INTERVAL)  # sleep
            data = self.package_data()  # get data to be sent
            if not self.send(self.serial_port, data):  # send
                print(f"{config.get_time()}: Failed to Send Data")
                self.vehicle.radio_state = 0
                self.serial_connect()  # attempt to reconnect if sending fails
            else:
                self.vehicle.radio_state = 2

            # exit
            if self.vehicle.exit:
                break