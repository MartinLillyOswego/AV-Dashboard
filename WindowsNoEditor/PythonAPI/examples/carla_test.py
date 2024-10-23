import glob
import os
import sys
import random
from time import sleep
import time
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla

# Create a list to hold actors
actor_list = []

# Try to connect to Carla host
try:
    client = carla.Client("localhost", 2000)
    client.set_timeout(5.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    # Create Model 3 Blueprint
    bp = blueprint_library.filter("model3")[0]
    print(bp)

    # Select random spawn point
    spawn_point = random.choice(world.get_map().get_spawn_points())

    # Spawn vehicle
    vehicle = world.spawn_actor(bp, spawn_point)

    # Add vehicle to actor list
    actor_list.append(vehicle)

    vehicle.set_autopilot(True)

    # This is the loop that will grab telemetry data and send it to the dashboard
    running = True
    start = time.time()
    while running:
        end = time.time()
        if (end - start) >= 30:
            running = False
        try:
            # Get the velocity vector of the vehicle and calculate speed
            velocity = vehicle.get_velocity()
            speed = 2.237 * (velocity.x**2 + velocity.y**2 + velocity.z**2)**0.5  # Speed in mph

            # Get the vehicle control for steering angle
            control = vehicle.get_control()
            physics_control = vehicle.get_physics_control()

            max_steer_angle = max(wheel.max_steer_angle for wheel in physics_control.wheels)
            
            # max_steer_angle = physics_control.wheels.WheelPhysicsControl(max_steer_angle)
            steering_angle = control.steer * max_steer_angle  # Approximating to degrees, -30 to +30 range

            print(f"Speed: {speed:.2f} mph | Steering Angle: {steering_angle:.2f} degrees")
            # print(f"Steering Angle: {steering_angle:.2f} degrees")
            # print(f"Wheel Speeds: {[f'{ws:.2f} mph' for ws in wheel_speeds]}")

        except Exception as e:
            print(f"Could not retrieve telemetry data: {e}")

        sleep(1)

# Destroy all actors before quitting
finally:
    for actor in actor_list:
        actor.destroy()
    print("done")
