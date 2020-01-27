# Kasey French
#
#
#
#
#
from numpy import reshape, array, zeros, random


class State(object):

	def __init__(self, pos =  zeros((2,1)), vel =  zeros((2,1))):

		self.pos = reshape(array(pos), (2,1))
		self.vel = reshape(array(vel), (2,1))


class Particle(object):

	def __init__(self, state = State()):

		self.state = state
		self.type = 'Particle'
		self.last_collision = ''

class MassiveParticle(Particle):

	def __init__(self, mass, state = State()):
		super(MassiveParticle, self).__init__(state)

		if mass <= 0:
			raise ValueError('Error in MassParticle(): mass must be positive!')

		self.mass = mass
		self.getType = random.random_integers(1,100000)








