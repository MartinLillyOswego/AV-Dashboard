"""
This is a test script that will spawn a Tesla Model 3 into Carla.
To use the script download Carla 9.8 and navigate to "[Carla folder]/WindowsNoEditor/PythonAPI/examples/" and place this file into this directory. Once Carla is running simply run the script.
Since the script is being run on the same computer you won't need to change the IP address, "localhost" will work.
"""
import glob
import os
import sys
import random
from time import sleep
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
    print("Spawn Point: " + str(spawn_point))

    # Spawn vehicle
    vehicle = world.spawn_actor(bp, spawn_point)

    # Add vehicle to actor list
    actor_list.append(vehicle)

    sleep(10)

# Destroy all actors before quitting
finally:
    for actor in actor_list:
        actor.destroy()
    print("done")
