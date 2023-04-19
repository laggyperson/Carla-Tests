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

	# Get blueprints and choose one for the NPCs
	blueprint_library = world.get_blueprint_library()
	npc_bp = blueprint_library['cybertruck']

    # Spawning NPCs in a row
    spawn_point = random.choice(world.get_map().get_spawn_points())
    for i in range(number_npcs):
        spawn_curr = spawn_point.location.x + (i * 4 - number_npcs / 2)
        npc = world.spawn(npc_bp, spawn_curr)
        actors.append(npc)

    # Moving NPCs by a little bit forwards
    while True:
        time.sleep(0.05) # The step length of the simulation in Sumo

        # Updating all NPC locations
        for c in actors:
            curr_pos = c.get_transform()
            curr_pos.location.y += 3
            c.set_transform(curr_pos)

        # Ticking the world
        world.tick()


if __name__ == '__main__':
	actors = []
	try:
		main()
	except KeyboardInterrupt:
		print('\nCancelled by user. Bye!')
	except RuntimeError as e:
		print(e)
	finally:
		print("Destroying all actors")
		for actor in actors:
			actor.destroy()
		print("Finished!")