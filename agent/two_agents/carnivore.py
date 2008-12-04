import math
import random
from PyQt4 import QtGui
from agent import agent

class carnivore(agent):
	def init(self):
		self.speed=30
		self.energy=1.0
		self.decay_rate=0.012
		self.spawn_prob=0.001
		self.type='carnivore'
		self.eat_prob=1
		self.brush=QtGui.QBrush(QtGui.QColor(255,0,0))
	def interract(self,other):
		if other.type=='herbivore' and not other.dead:
			other.dead=True
			self.energy+=0.65
