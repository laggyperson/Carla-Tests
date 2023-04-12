""" Telepaorts carla ego vehicle continuously every n seconds, specified when called with '-n <number>'
Default teleport every 10 seconds
Vehicle will be controlled by Carla autopilot.
Coded for Python 2.7 (to the best of my ability)

Author: Phillip Chen and whoever wrote all the other Carla Python files"""

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
	# Creating argparser object
	argparser = argparse.ArgumentParser(description='Spawns a single ego vehicle and teleports it every n seconds. Will default to 10.0 seconds.')

	argparser.add_argument(
		'-n', 
		metavar='N', 
		default=10.0,
		type=float,
		dest='n', 
		help='Time (double) between teleports for ego vehicle. Default 10.0 seconds')

	# Need to specify time between each teleportation
	if len(sys.argv) < 1:
		argparser.print_help()
		return

	# Should only be length 1
	args = argparser.parse_args()
	teleport_time = args.n

	# Accessing Carla server
	client = carla.Client('localhost', 2000)
	client.set_timeout(4.0)

	# Load in world
	world = client.get_world()

	# Get blueprints and choose one at random fro ego vehicle
	blueprint_library = world.get_blueprint_library()
	ego_bp = random.choice(blueprint_library.filter('vehicle'))

	# Get random spawn point.
	spawn = random.choice(world.get_map().get_spawn_points())

	# Create vehicle
	vehicle = world.try_spawn_actor(ego_bp, spawn)
	actors.append(vehicle)
	vehicle.set_autopilot(True)
	print("Spawned %s" % vehicle.type_id)

	# Crude way of teleporting vehicle every n seconds
	while True:
		time.sleep(teleport_time)
		vehicle.set_transform(random.choice(world.get_map().get_spawn_points()))
		print("Teleported at %s" % time.asctime(time.localtime()))


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