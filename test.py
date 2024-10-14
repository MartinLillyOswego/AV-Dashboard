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

actor_list = []

try:
    client = carla.Client("localhost", 2000)
    client.set_timeout(5.0)
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    bp = blueprint_library.filter("model3")[0]
    print(bp)

    spawn_point = random.choice(world.get_map().get_spawn_points())
    print("Spawn Point: " + str(spawn_point))

    vehicle = world.spawn_actor(bp, spawn_point)

    actor_list.append(vehicle)

    sleep(10)

finally:
    for actor in actor_list:
        actor.destroy()
    print("done")