# Kasey French
# Sept 27th 2018
#
# Particles in Box Game
#
#
#
#

from ElasticParticles2 import *
import numpy as np
import graphics
import time
import pygame

def main():


	pygame.init()
	playing = True
	move_ticker = 0

	MAP_SIZE = 400
	my_particle_list = []
	my_circle_list = []
	t = 0

	win = graphics.GraphWin('My MAP', MAP_SIZE, MAP_SIZE, autoflush = False)

	player = MassiveParticle(4, State(pos = np.array([[MAP_SIZE / 2],[MAP_SIZE / 2]]), vel = np.array([[0],[0]])))

	for i in range(6):
		my_particle_list.append(MassiveParticle(4, State(pos =  np.array([[MAP_SIZE / 2],[MAP_SIZE / 2]]) +
																				 np.array([[np.random.randint(- MAP_SIZE / 2, MAP_SIZE / 2)],
																				 [np.random.randint(- MAP_SIZE / 2, MAP_SIZE / 2)]]),
		                                     vel = 3 * np.random.randn(2,1))))

		my_circle_list.append(graphics.Circle(graphics.Point(my_particle_list[i].state.pos[0][0],
		                                                    my_particle_list[i].state.pos[1][0]),
																				my_particle_list[i].mass))




	for circle in my_circle_list:
		circle.setFill("Black")
		circle.draw(win)

	player_circle = graphics.Circle(graphics.Point(player.state.pos[0][0], player.state.pos[1][0]), player.mass)
	player_circle.setFill('Red')
	player_circle.draw(win)

	my_particle_list.append(player)
	my_circle_list.append(player_circle)

	while playing == True:

		move_ticker = update_player(player, player_circle, move_ticker)
		print(move_ticker)

		for part in my_particle_list:

			i = my_particle_list.index(part)
			old_pos = part.state.pos
			part.state.pos = part.state.pos + part.state.vel
			my_circle_list[i].move(part.state.pos[0][0] - old_pos[0][0], part.state.pos[1][0] - old_pos[1][0])
			# point_list[i].move(part.state.pos[0][0] - old_pos[0][0], part.state.pos[1][0] - old_pos[1][0])

			if part.state.pos[0][0] + part.mass >= MAP_SIZE - MAP_SIZE * .01 and part.state.vel[0][0] > 0:
				part.state.vel[0][0] = - part.state.vel[0][0]
				part.last_collision = part.type

			if part.state.pos[1][0] + part.mass >= MAP_SIZE - MAP_SIZE * .01 and part.state.vel[1][0] > 0:
				part.state.vel[1][0] = - part.state.vel[1][0]
				part.last_collision = part.type

			if part.state.pos[0][0] - part.mass <= MAP_SIZE * .01 and part.state.vel[0][0] < 0:
				part.state.vel[0][0] = - part.state.vel[0][0]
				part.last_collision = part.type

			if part.state.pos[1][0] - part.mass <= MAP_SIZE * .01 and part.state.vel[1][0] < 0:
				part.state.vel[1][0] = - part.state.vel[1][0]
				part.last_collision = part.type


		for part1 in my_particle_list:

			for part2 in my_particle_list:

				if my_particle_list.index(part1) >= my_particle_list.index(part2):
					continue

				if part1.last_collision == part2.getType() and part2.last_collision == part1.getType():

					continue


				elif np.abs(np.linalg.norm(part1.state.pos - part2.state.pos)) <= (part1.mass + part2.mass):

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

					part1.state.vel = (part1.state.vel - (2 * m2 / (m1 + m2)) *
														(inner1 * (part1.state.pos - part2.state.pos) /
														(np.linalg.norm(part1.state.pos - part2.state.pos) ** 2)))

					part2.state.vel = (part2.state.vel - (2 * m1 / (m1 + m2)) *
														(inner2 * (part2.state.pos - part1.state.pos) /
														(np.linalg.norm(part2.state.pos - part1.state.pos) ** 2)))


					part2.last_collision = part1.getType()
					part1.last_collision = part2.getType()



		win.update()
		time.sleep(.01)
		t += 1

def update_player(player = MassiveParticle(1, State(pos = 200 * np.ones((2,1)),
                                                 vel = np.zeros((2,1)))),
									player_circle = graphics.Circle(graphics.Point(0,0), 10), move_ticker = 0):

	Speed = 2
	pygame.event.pump()
	events = pygame.event.get()

	if move_ticker <= 0:

		for event in events:

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_UP:
					player.state.vel -= np.array([[0],[Speed]])
					move_ticker = 10

				elif event.key == pygame.K_DOWN:
					player.state.vel += np.array([[0],[Speed]])
					move_ticker = 10

				elif event.key == pygame.K_RIGHT:
					player.state.vel += np.array([[Speed],[0]])
					move_ticker = 10

				elif event.key == pygame.K_LEFT:
					player.state.vel -= np.array([[Speed],[0]])
					move_ticker = 10

	else:
		move_ticker -= 1

	return move_ticker

	# pygame.event.clear()

main()


