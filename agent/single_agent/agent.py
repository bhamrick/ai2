import copy
import math
import random
from PyQt4 import QtGui

class agent:
	def __init__(self,world):
		self.type=''
		self.x = random.random()*world.width
		self.y = random.random()*world.height
		self.world=world
		self.dead=False
		self.radius = 5
		self.brush=QtGui.QBrush(QtGui.QColor(0,0,255))
		self.age=0
		self.init()
	def init(self):
		self.speed=5
		self.energy=1.0
		self.decay_rate=0.05
		self.spawn_prob=0.01
	def move(self):
		self.age+=1
		r = random.random()*self.speed
		theta = random.random()*2*math.pi
		dx = r*math.cos(theta)
		dy = r*math.sin(theta)
		if self.world.type == 'spherical':
			radius = self.world.height/2.0
			y = radius - self.y
			dx /= max(math.sqrt(1-y*y/(radius*radius)),0.00000001)
		self.x+=dx
		self.y+=dy
		if self.world.type == 'spherical':
			self.x%=self.world.width
			self.y%=2*self.world.height
			if self.y > self.world.height:
				self.y = 2*self.world.height-self.y
		if self.world.type == 'toroidal':
			self.x%=self.world.width
			self.y%=self.world.height
		if self.world.type == 'bounded':
			if self.x < 0.0:
				self.x = 0.0
			if self.y < 0.0:
				self.y = 0.0
			if self.x > self.world.width:
				self.x = self.world.width
			if self.y > self.world.height:
				self.y = self.world.height
		self.energy -= self.decay_rate
		self.try_to_eat()
		self.try_to_spawn()
		self.check_if_dead()
	def try_to_eat(self):
		pass
	def try_to_spawn(self):
		if random.random() < self.spawn_prob*self.energy:
			self.world.agents.append(copy.copy(self))
			self.world.agents[-1].energy = 1.0
			self.world.agents[-1].age=0
	def interract(self,other):
		pass
	def check_if_dead(self):
		if self.energy <= 0.0:
			self.dead=True
