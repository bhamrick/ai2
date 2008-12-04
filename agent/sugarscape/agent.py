import copy
import math
import random
from PyQt4 import QtGui

class agent:
	def __init__(self,world,id=-1):
		self.type=''
		self.id = id
		self.x = int(random.random()*world.width)
		self.y = int(random.random()*world.height)
		while world.agents[self.x][self.y]!=None:
			self.x = int(random.random()*world.width)
			self.y = int(random.random()*world.height)
		world.agents[self.x][self.y] = self
		world.agent_list.append(self)
		self.world=world
		self.dead=False
		self.color=QtGui.QColor(0,0,255)
		self.age=0
		self.init()
		self.vision=0
		self.metabolism=0
		self.wealth=0
		self.init()
	def init(self):
		self.vision=int(random.random()*6+1)
		self.metabolism=int(random.random()*4)+1
		self.wealth=10
	def move(self):
		count = 1
		bestx = self.x
		besty = self.y
		best = self.world.sugar[self.x][self.y]
		bestd = 0
		for i in range(self.vision+1):
			if self.x+i < self.world.width:
				if self.world.agents[self.x+i][self.y]==None:
					if self.world.sugar[self.x+i][self.y] > best:
						best = self.world.sugar[self.x+i][self.y]
						count = 1
						bestx = self.x+i
						besty = self.y
						bestd = i
					elif self.world.sugar[self.x+i][self.y] == best:
						if i == bestd:
							count+=1
							if random.random()<1.0/count:
								bestx=self.x+i
								besty=self.y
			if self.x-i >= 0:
				if self.world.agents[self.x-i][self.y]==None:
					if self.world.sugar[self.x-i][self.y] > best:
						best = self.world.sugar[self.x-i][self.y]
						count = 1
						bestx = self.x-i
						besty = self.y
						bestd = i
					elif self.world.sugar[self.x-i][self.y] == best:
						if i == bestd:
							count+=1
							if random.random()<1.0/count:
								bestx=self.x-i
								besty=self.y
			if self.y+i < self.world.height:
				if self.world.agents[self.x][self.y+i]==None:
					if self.world.sugar[self.x][self.y+i] > best:
						best = self.world.sugar[self.x][self.y+i]
						count = 1
						bestx = self.x
						besty = self.y+i
						bestd = i
					elif self.world.sugar[self.x][self.y+i] == best:
						if i == bestd:
							count+=1
							if random.random()<1.0/count:
								bestx=self.x
								besty=self.y+i
			if self.y-i >= 0:
				if self.world.agents[self.x][self.y-i]==None:
					if self.world.sugar[self.x][self.y-i] > best:
						best = self.world.sugar[self.x][self.y-i]
						count = 1
						bestx = self.x
						besty = self.y-i
						bestd = i
					elif self.world.sugar[self.x][self.y-i] == best:
						if i == bestd:
							count+=1
							if random.random()<1.0/count:
								bestx=self.x
								besty=self.y-i
		self.world.agents[self.x][self.y]=None
		self.x=bestx
		self.y=besty
		self.world.agents[self.x][self.y]=self
		self.wealth-=self.metabolism
	def harvest(self):
		self.wealth+=self.world.sugar[self.x][self.y]
		self.world.sugar[self.x][self.y]=0
	def try_to_spawn(self):
		pass
	def interract(self,other):
		pass
	def check_if_dead(self):
		if self.wealth < 0:
			self.dead=True
