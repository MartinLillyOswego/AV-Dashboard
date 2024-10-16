"""
!!WARNING!!
Due to this project using Carla 9.8 this script requires Python 3.7 in order to work with the Carla host and the Carla python package.
Once Python 3.7 is installed use pip to install the Carla package "pip install carla==0.9.5" (this command may result in errors but does not affect performance)
!!WARNING!!

This is a test script that will spawn a Tesla Model 3 into Carla with autopilot enabled. The vhicle seep will be printed every .025 seconds for 30 seconds then the car will
be destoyed.

To use the script download Carla 9.8 and navigate to "[Carla folder]/WindowsNoEditor/PythonAPI/examples/" and place this file into this directory.
Once Carla is running simply run the script.
Since the script is being run on the same computer you won't need to change the IP address, "localhost" will work.

Note: Carla simulator 9.8 requires at least 4GB of dedicated video memory to run properly.
"""
from threading import Thread
from time import sleep
import threading
import Vehicle
import random
import config
import glob
import time
import sys
import os

class CarlaVehicle(threading.Thread):

    def __init__(self, vehicle, *args, **kwargs):
        super(CarlaVehicle, self).__init__(*args, **kwargs)
        self.vehicle = vehicle

    def run(self):
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
            client = carla.Client("127.0.0.1", 2000)
            client.set_timeout(5.0)
            world = client.get_world()
            blueprint_library = world.get_blueprint_library()

            # Create Modle 3 Blueprint
            bp = blueprint_library.filter("model3")[0]
            print(f"{config.get_time()}:CarlaVehicle: {bp}")

            # Select random spawn point
            spawn_point = random.choice(world.get_map().get_spawn_points())

            # Spawn vehicle
            vehicle = world.spawn_actor(bp, spawn_point)

            # Add vehicle to actor list
            actor_list.append(vehicle)

            vehicle.set_autopilot(True)

            # This is the loop that will grab telementry data and send it to the dashboard
            running = True
            start = time.time()  # Start timer for runtime
            while running:
                 end = time.time()
                if (end - start) >= 30:
                    running = False
                try:
                    # Get the velocity vector of the vehicle and calculate speed
                    velocity = vehicle.get_velocity()
                    speed = 2.237 * (velocity.x ** 2 + velocity.y ** 2 + velocity.z ** 2) ** 0.5  # Speed in mph

                    # Get the vehicle control for steering angle
                    control = vehicle.get_control()
                    physics_control = vehicle.get_physics_control()

                    max_steer_angle = max(wheel.max_steer_angle for wheel in physics_control.wheels)
                    steering_angle = control.steer * max_steer_angle  # Approximating to degrees, -30 to +30 range

                    # update the vehicle class with vehicle.update_with_packet()
                    atts = [12, 24, speed, 0.43, 0, steering_angle, 4.325, 0, 45.3, 25.4, 23.8, 257.23, 180, time.time()]
                    self.vehicle.update_with_packet(atts)

                    #print(f"Speed: {speed:.2f} mph | Steering Angle: {steering_angle:.2f} degrees")
                    # print(f"Steering Angle: {steering_angle:.2f} degrees")
                    # print(f"Wheel Speeds: {[f'{ws:.2f} mph' for ws in wheel_speeds]}")

                except Exception as e:
                    print(f"Could not retrieve telemetry data: {e}")

                sleep(1)

        # Destroy all actors before quitting
        finally:
            for actor in actor_list:
                actor.destroy()
            print(f"{config.get_time()}:CarlaVehicle: Done")
