import math
import random
from linegraph import linegraph
from PyQt4 import QtGui, QtCore

class world(QtGui.QWidget):
	def __init__(self, width, height, type='spherical', parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.agents=[]
		self.width=width
		self.height=height
		self.resize(width,height)
		self.setWindowTitle('Agent Modeling World')
		if type != 'bounded' and type != 'spherical' and type != 'toroidal':
			self.type='spherical'
		else:
			self.type=type
		self.food = []
		self.food_granularity=8
		self.interract_granularity=10
		for i in range(self.width/self.food_granularity):
			self.food.append([])
			for j in range(self.height/self.food_granularity):
				self.food[i].append(False)
		self.food_spawn_prob = 0.03
		self.food_rot_prob = 0.1
		self.timer = QtCore.QTimer()
		self.timer.setSingleShot(False)
		self.connect(self.timer,QtCore.SIGNAL('timeout()'),self,QtCore.SLOT('update()'))
		self.timer.start(1)
		self.generation=0
		for i in range(10):
			self.spawn_food()
		self.pop_plot = linegraph(1000,2)
		self.pop_plot.setcolor(0,QtGui.QColor(0,255,0))
		self.pop_plot.setcolor(1,QtGui.QColor(255,0,0))
		self.pop_plot.setWindowTitle('Population')
		self.pop_plot.show()
	def spawn_food(self):
		for i in range(self.width/self.food_granularity):
			for j in range(self.height/self.food_granularity):
				if not self.food[i][j]:
					if random.random() < self.food_spawn_prob:
						self.food[i][j]=True
				else:
					if random.random() < self.food_rot_prob:
						self.food[i][j]=False
	def run_generation(self):
		self.generation+=1
		self.spawn_food()
		for agent in self.agents:
			agent.move()
		interractions=[]
		for i in range(self.width/self.interract_granularity):
			interractions.append([])
			for j in range(self.height/self.interract_granularity):
				interractions[i].append([])
		for agent in self.agents:
			interractions[int(agent.x/self.interract_granularity)][int(agent.y/self.interract_granularity)].append(agent)
		for i in range(self.width/self.interract_granularity):
			for j in range(self.height/self.interract_granularity):
				for agent1 in interractions[i][j]:
					for agent2 in interractions[i][j]:
						agent1.interract(agent2)
		new_gen = []
		for agent in self.agents:
			if not agent.dead:
				new_gen.append(agent)
		self.agents=new_gen
	def paintEvent(self,event):
		self.run_generation()
		paint = QtGui.QPainter()
		paint.begin(self)
		for agent in self.agents:
			paint.setBrush(agent.brush)
			paint.drawEllipse(agent.x-agent.radius,agent.y-agent.radius,2*agent.radius,2*agent.radius)
		paint.end()
		herbs = 0
		carns = 0
		for agent in self.agents:
			if agent.type=='herbivore':
				herbs+=1
			if agent.type=='carnivore':
				carns+=1
		#print self.generation, herbs, carns
		self.pop_plot.addval(0,herbs)
		self.pop_plot.addval(1,carns)
		self.pop_plot.inc()
		self.pop_plot.update()
