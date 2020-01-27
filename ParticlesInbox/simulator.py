
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np


class simulator(object):

	def __init__(self, particleList):
		self.particleList = particleList
		self.labels = []
		self.tspan = np.linspace(1,10000, 500)
		for part in particleList:
			self.labels.append(part.getType)

	def animate2D(self, xlim, ylim, nframes = None, labels = {}):

		if nframes is None:
			nframes = len(self.tspan)
		self.count = 0

		def plotFrame(n):

			#print('Animating frame %d of %d' % (self.count, nframes), end = '\r')
			fig.clear()
			self.count += 1

			for k, part in self.particleList.iteritems():

				x = part[n][0]
				y = part[n][1]
				plt.plot(x, y, '.')

				ax = plt.subplot()
				ax.set_aspect('equal', adjustable = 'box')
				ax.set_ylim(0, ylim)
				ax.set_xlim(0, xlim)

			plt.legend(loc = 'upper center', bbox_to_anchor = (0.5, 1.1),
	           ncol = 5, fancybox = True, shadow = True,
	           frameon = True, fontsize = 8)

		fig = plt.figure()
		n = len(self.tspan)
		# print(n)
		# print(nframes)
		frames = range(0, n, int(n / nframes))
		nframes = len(frames)

		anim = animation.FuncAnimation(fig, plotFrame, frames = frames, blit = False)

		Writer = animation.writers['ffmpeg']
		writer = Writer(fps = 60, bitrate = 1800)
		anim.save('Elastic.mp4', writer = writer)
		print('\n')



