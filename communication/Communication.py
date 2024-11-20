from control.Vehicle import Vehicle
import serial.tools.list_ports
import control.config as config
import threading
import serial
import time
from control.Controller import Controller

class Communication(threading.Thread):

    def __init__(self, vehicle):
        super(Receiver, self).__init__()
        self.vehicle = vehicle
        self.serial_port = None
        self.controller = Controller()

    def serial_connect(self):
        while True:
            serial_id = config.VEHICLE_PORT
            try:
                self.serial_port = serial.Serial(serial_id, baudrate=115200, timeout=1)
                if not self.serial_port.is_open:
                    self.serial_port.open()
                print(f"{config.get_time()}:Receiver: Serial port connected")
                break
            except serial.SerialException as e:
                print(f"{config.get_time()}:Receiver: Failed to connect to serial port {e}")
                time.sleep(config.SEND_INTERVAL)

    def package_data(self):
        # pull last_packet from vehicle class
        vehicle_snapshot = self.vehicle.__copy__()
        ind = len(vehicle_snapshot.speed) - 1
        
        # If no data is available yet
        if ind == -1:
            return None

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
        packetToSend += bytes(new_commands)
        
        return packetToSend

    @staticmethod
    def send(connection, data):
        if (data is None) or (connection is None):
            return False
        try:
            #print("send: " + str(data))
            connection.write(data)
        except serial.SerialTimeoutException:
            print(f"{config.get_time()}:SendingThread: Failed to send packet, bad serial connection")
            return False
        return True

    # main loop
    def run(self):
        # Connect to serial port
        self.serial_connect()
        while True:
            while not self.serial_port or not self.serial_port.in_waiting:
                pass
            # Read Packet
            packet = self.serial_port.read(config.PACKET_SIZE)
            
            # Update Packet
            self.vehicle.update_with_packet(packet)
            
            # Call send method 
            self.send(self.serial_port, self.package_data())
            
            # Exit
            if self.vehicle.exit:
                break


