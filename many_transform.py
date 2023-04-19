""" 
Testing how well the transform command works in Carla by teleporting many vehicles at once.

Author: Phillip Chen
Date: April 2023
"""

import glob
import os
import sys
import argparse
import time
import random

# Importing CARLA
try:
	sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
		sys.version_info.major,
		sys.version_info.minor,
		'win-amd64' if os.name =='nt' else 'linux-x86_64'))[0])
except IndexError:
	print("Couldn't find Carla")
	pass

import carla

def main():
    argparser = argparse.ArgumentParser(description='Takes in argument for how many cars to teleport at once.')
    argparser.add_argument(
        '-n',
        metavar='N', 
		default=100,
		type=int,
		dest='n', 
		help='Number of cars to teleport'
    )

    args = argparser.parse_args()
    number_npcs = args.n
    
	# Accessing Carla server
    client = carla.Client('localhost', 2000)
    client.set_timeout(4.0)

    # Load in world
    world = client.get_world()
    
    # Turning on Synchronous mode to control tick of world
    settings = world.get_settings()
    settings.synchronous_mode = True

    # Get blueprints and choose one for the NPCs
    blueprint_library = world.get_blueprint_library()
    npc_bp = random.choice(blueprint_library.filter('cybertruck'))

    # Spawning NPCs in a row
    spawn_point = random.choice(world.get_map().get_spawn_points())
    spawn_point.location.z += 50
    for i in range(number_npcs):
        spawn_curr = random.choice(world.get_map().get_spawn_points())
        spawn_curr.location.x = spawn_point.location.x + (i - number_npcs / 2) * 10
        spawn_curr.location.y = spawn_point.location.y
        spawn_curr.location.z = spawn_point.location.z
        spawn_curr.rotation = spawn_point.rotation
        npc = world.try_spawn_actor(npc_bp, spawn_curr)
        if not (npc == None):
            npc.set_simulate_physics(False)
            print("Spawned actor {} at: x: {}, y: {}, z: {}".format(i, spawn_curr.location.x, spawn_curr.location.y, spawn_curr.location.z))
            actors.append(npc)
    
    num_spawned = len(actors) # Keeps track of how many vehicles actually spawned

    # Moving NPCs by a little bit forwards
    while True:
        time.sleep(0.05) # The step length of the simulation in Sumo

        # Updating all NPC locations
        print("############################ MOVING {} ACTORS #################################".format(num_spawned))
        for c in actors:
            curr_pos = c.get_transform()
            curr_pos.location.y += 3
            c.set_transform(curr_pos)
            print("Moved NPC to: x: {}, y: {}, z: {}".format(spawn_curr.location.x, spawn_curr.location.y, spawn_curr.location.z))
        # Ticking the world
        world.tick()


if __name__ == '__main__':
    actors = []
    try:
        time_start = time.time()
        main()
    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
    except RuntimeError as e:
        print(e)
    finally:
        time_end = time.time()
        print("Time elapsed: ", time_end - time_start)
        print("Destroying {} actors".format(len(actors)))
        for actor in actors:
            actor.destroy()
        print("Finished!")