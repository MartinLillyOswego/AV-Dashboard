import time
from Vehicle import Vehicle

def park_packet(vehicle):
    return [
        vehicle.sender_id,
        vehicle.receiver_id,
        0,  # error code
        0.0,  # velocity
        0.0,  # throttle
        0.0,  # braking force
        100,  # hand brake
        0.0,  # steering angle
        0.0,  # direction
        0,  # gear
        vehicle.battery_voltage,  # battery voltage
        vehicle.battery_current,  # battery current
        vehicle.battery_temperate,  # battery temperature
        0.0,  # left wheel speed
        0.0,  # right wheel speed
        vehicle.distance_to_object,  # distance to object
        0.0   # time
    ]


def slowdown(vehicle, decrement=5):

    if (vehicle.velocity > 0):
        vehicle.velocity = max(vehicle.velocity - decrement, 0.0)
        vehicle.throttle = 0.0
        vehicle.braking_force = 10

def shutdown(receiver, sender, vehicle):
    print("Initiating shutdown sequence...")

    # Slow down the vehicle before shutting down
    while(vehicle.velocity > 0):
        slowdown(vehicle)
        sender.send(receiver.serial_port,vehicle)


    print("Sending park packet...")
    park_data = park_packet(vehicle)

    if sender.send(receiver.serial_port, park_data):
        print("Park packet sent.")

    vehicle.exit = True    #assuming this is in control_unit

    receiver.join()
    sender.join()
    print("Shutdown complete.")