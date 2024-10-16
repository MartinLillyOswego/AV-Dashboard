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

    # Create Modle 3 Blueprint
    bp = blueprint_library.filter("model3")[0]
    print(bp)

    # Select random spawn point
    spawn_point = random.choice(world.get_map().get_spawn_points())

    # Spawn vehicle
    vehicle = world.spawn_actor(bp, spawn_point)

    # Add vehicle to actor list
    actor_list.append(vehicle)

    vehicle.set_autopilot(True)

    # This is the loop that will grab telementry data and send it to the dashboard
    running = True
    start = time.time() # Start timer for runtime
    while running:
        end = time.time()
        if (end - start) >= 30: running = False # Stop loop after 30 seconds
        # Get the velocity vector of the vehicle
        velocity = vehicle.get_velocity()

        # Convert velocity to speed (magnitude)
        Covervion_factor = 2.237 # Use 2.237 for MPH and 3.6 for KPH
        speed = Covervion_factor * (velocity.x**2 + velocity.y**2 + velocity.z**2)**0.5
        
        print(f"Speed: {speed:.2f} MPH")
        sleep(.025)

# Destroy all actors before quitting
finally:
    for actor in actor_list:
        actor.destroy()
    print("done")
