import math
import random
from PyQt4 import QtGui
from agent import agent

class herbivore(agent):
	def init(self):
		self.speed=15
		self.energy=1.0
		self.decay_rate=0.05
		self.spawn_prob=0.01
		self.type='herbivore'
		self.eat_prob=1
		self.brush = QtGui.QBrush(QtGui.QColor(0,0,255))
	def try_to_eat(self):
		if self.world.food[int(self.x)/self.world.food_granularity][int(self.y)/self.world.food_granularity]:
			if random.random() < self.eat_prob:
				self.world.food[int(self.x)/self.world.food_granularity][int(self.y)/self.world.food_granularity]=False
				self.energy+=0.305
