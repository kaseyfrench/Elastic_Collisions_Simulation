# Kasey French
#
# Sept. 21 2018
# Particles in a Box

# Check if circles and particles list locations are identical!!1111111


import numpy as np
import graphics
import time
from ElasticParticles2 import *
from simulator import *

MAP_SIZE = 500
PARTICLE_SIZE = 2


def main():

	win = graphics.GraphWin('Particles in a Box', MAP_SIZE, MAP_SIZE, autoflush = False)

	number = raw_input("How may particles should we put in the box? ")

	if not number.isdigit():
		raise ValueError("Input must be an integer! ")

	number = int(number)

	particle_list = []
	circle_list = []
	point_list = []
	stateList = {}

	t = 0

	for i in range(number):
		particle_list.append(MassiveParticle(np.random.uniform(1,5),
		                                     State(pos =  np.array([[MAP_SIZE / 2],[MAP_SIZE / 2]]) +
																				 np.array([[np.random.randint(- MAP_SIZE / 2, MAP_SIZE / 2)],
																				 [np.random.randint(- MAP_SIZE / 2, MAP_SIZE / 2)]]),
		                                     vel = 5 * np.random.randn(2,1))))

		for part in particle_list:
			stateList[part] = []

			if part == particle_list[i]:
				break

			while np.linalg.norm(particle_list[i].state.pos - part.state.pos) <= (part.mass + particle_list[i].mass) * PARTICLE_SIZE:
				particle_list[i].state.pos = np.array([[np.random.randint(- MAP_SIZE / 2, MAP_SIZE / 2)], [np.random.randint(- MAP_SIZE / 2, MAP_SIZE / 2)]])

		circle_list.append(graphics.Circle(graphics.Point(particle_list[i].state.pos[0][0],
		                                                  particle_list[i].state.pos[1][0]),
																											particle_list[i].mass * PARTICLE_SIZE ))

		# point_list.append(graphics.Point(particle_list[i].state.pos[0][0],
		#                                                  particle_list[i].state.pos[1][0]))

	for circle in circle_list:
		circle.setFill("Black")
		circle.draw(win)

	for point in point_list:
		point.draw(win)

	total_momentum_bef = 0
	total_momentum_aft = 0

	inner_pro_2 = 0
	inner_pro_1 = 0
	inner_pro_3 = 0
	inner_pro_4 = 0

	m1 = 0
	m2 = 0

	energy_bef = 0
	energy_aft = 0

	collisions = 0

	inner1 = 0
	inner2 = 0
	count = 0

	for part in particle_list:

		total_momentum_bef += part.mass * part.state.vel
		energy_bef += .5 * part.mass * (part.state.vel[1][0] ** 2 + part.state.vel[0][0] ** 2)


	while t <= 1000:
		for part in particle_list:
			stateList[part].append(part.state.pos)
			count += 1

		for part in particle_list:

			i = particle_list.index(part)
			old_pos = part.state.pos
			part.state.pos = part.state.pos + part.state.vel
			circle_list[i].move(part.state.pos[0][0] - old_pos[0][0], part.state.pos[1][0] - old_pos[1][0])
			# point_list[i].move(part.state.pos[0][0] - old_pos[0][0], part.state.pos[1][0] - old_pos[1][0])

			if part.state.pos[0][0] + part.mass * PARTICLE_SIZE >= MAP_SIZE - MAP_SIZE * .01 and part.state.vel[0][0] > 0:
				part.state.vel[0][0] = - part.state.vel[0][0]
				part.last_collision = part.type

			if part.state.pos[1][0] + part.mass * PARTICLE_SIZE >= MAP_SIZE - MAP_SIZE * .01 and part.state.vel[1][0] > 0:
				part.state.vel[1][0] = - part.state.vel[1][0]
				part.last_collision = part.type

			if part.state.pos[0][0] - part.mass * PARTICLE_SIZE <= MAP_SIZE * .01 and part.state.vel[0][0] < 0:
				part.state.vel[0][0] = - part.state.vel[0][0]
				part.last_collision = part.type

			if part.state.pos[1][0] - part.mass * PARTICLE_SIZE <= MAP_SIZE * .01 and part.state.vel[1][0] < 0:
				part.state.vel[1][0] = - part.state.vel[1][0]
				part.last_collision = part.type

		for part1 in particle_list:

			for part2 in particle_list:

				if particle_list.index(part1) >= particle_list.index(part2):
					continue

				if part1.last_collision == part2.getType and part2.last_collision == part1.getType:

					continue


				elif np.abs(np.linalg.norm(part1.state.pos - part2.state.pos)) <= (part1.mass + part2.mass) * PARTICLE_SIZE:

					m1 = part1.mass
					m2 = part2.mass

					inner_pro_1 = part1.state.vel - part2.state.vel
					inner_pro_2 = part1.state.pos - part2.state.pos
					inner_pro_3 = part2.state.vel - part1.state.vel
					inner_pro_4 = part2.state.pos - part1.state.pos

					inner_pro_1 = np.reshape(inner_pro_1, (1,2))
					inner_pro_3 = np.reshape(inner_pro_3, (1,2))

					inner1 = (np.dot(inner_pro_1, inner_pro_2))
					inner2 = (np.dot(inner_pro_3, inner_pro_4))

					momentum_bef_col = part1.mass * part1.state.vel + part2.mass * part2.state.vel

					part1.state.vel = (part1.state.vel - (2 * m2 / (m1 + m2)) *
														(inner1 * (part1.state.pos - part2.state.pos) /
														(np.linalg.norm(part1.state.pos - part2.state.pos) ** 2)))

					part2.state.vel = (part2.state.vel - (2 * m1 / (m1 + m2)) *
														(inner2 * (part2.state.pos - part1.state.pos) /
														(np.linalg.norm(part2.state.pos - part1.state.pos) ** 2)))

					momentum_aft_col = part1.mass * part1.state.vel + part2.mass * part2.state.vel

					part2.last_collision = part1.getType
					part1.last_collision = part2.getType
					print('P Bef Col: ' + str(momentum_bef_col))
					print('P Aft Col: ' + str(momentum_aft_col))
					print('')

					# time.sleep(.1)
					# print('Time: ' + str(t))
					collisions += 1

					for part in particle_list:

						total_momentum_aft += np.abs(part.state.vel)

					total_momentum_aft = 0

		win.update()
		time.sleep(.01)
		t += 1

	print('Collisions: ' + str(collisions))

	for part in particle_list:

		total_momentum_aft += part.state.vel
		energy_aft += .5 * part.mass * (part.state.vel[1][0] ** 2 + part.state.vel[0][0] ** 2)

	#print('total_momentum_aft: ' + str(total_momentum_aft))
	#print('')
	#print('total_momentum_bef: ' + str(total_momentum_bef))
	#print('')
	print('Energy Before: ' + str(energy_bef))
	print('Energy After: ' + str(energy_aft))

	#print('Energy From Momentum After: ' + str(.5 * (total_momentum_aft[0][0] ** 2 + total_momentum_aft[1][0] ** 2)))
	#print('Energy From Momentum Before: ' + str(.5 * (total_momentum_bef[0][0] ** 2 + total_momentum_bef[1][0] ** 2)))
	mySim = simulator(stateList)
	mySim.animate2D(500,500,count / 50)

main()



# p1 + p2 = p1' + p2'
# E1' + E2' = E1 + E2
#
# (1 1)     (m1* v1) = (1 1)    (m1 * v1')
# (v1 v2) (m2 * v2) = (v1' v2') (v1' v2')
#
#
#
#

