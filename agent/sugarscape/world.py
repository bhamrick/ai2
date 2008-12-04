import math
import random
from linegraph import linegraph
from PyQt4 import QtGui, QtCore

class world(QtGui.QWidget):
	def __init__(self, sugar_map, parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
		self.agents=[]
		self.agent_list=[]
		self.width=sugar_map.mwidth
		self.height=sugar_map.mheight
		self.cell_size = 8
		self.setFixedSize(self.width*self.cell_size,self.height*self.cell_size)
		self.setWindowTitle('Sugarscape')
		self.sugar = []
		self.sugar_map = sugar_map
		self.sugar_cap = self.sugar_map.current()
		self.previouslyDrawn = []
		for i in range(self.width):
			self.agents.append([])
			self.sugar.append([])
			self.previouslyDrawn.append([])
			for j in range(self.height):
				self.sugar[i].append(self.sugar_cap[i][j])
				self.agents[i].append(None)
				self.previouslyDrawn[i].append(-1)
		self.timer = QtCore.QTimer()
		self.timer.setSingleShot(False)
		self.connect(self.timer,QtCore.SIGNAL('timeout()'),self,QtCore.SLOT('update()'))
		self.timer.start(00)
		self.generation=0
		self.pop_plot = linegraph(400)
		self.pop_plot.setWindowTitle('Population')
		self.pop_plot.show()
	def spawn_sugar(self):
		for i in range(self.width):
			for j in range(self.height):
				self.sugar[i][j]=max(self.sugar[i][j],min(self.sugar_cap[i][j],self.sugar[i][j]+1))
	def run_generation(self):
		self.pop_plot.addval(0,len(self.agent_list))
		self.pop_plot.inc()
		self.generation+=1
		n = len(self.agent_list)
		while n > 1:
			k = int(random.random()*(n))
			n-=1
			temp = self.agent_list[n]
			self.agent_list[n]=self.agent_list[k]
			self.agent_list[k]=temp
		for agent in self.agent_list:
			agent.harvest()
			agent.move()
			agent.check_if_dead()
		self.spawn_sugar()
		new_gen = []
		for agent in self.agent_list:
			if not agent.dead:
				new_gen.append(agent)
			else:
				self.agents[agent.x][agent.y]=None
		self.agent_list=new_gen
		self.sugar_map.step()
		self.sugar_cap = self.sugar_map.current()
	def paintEvent(self,event):
		self.run_generation()
		paint = QtGui.QPainter()
		paint.begin(self)
		for i in range(self.width):
			for j in range(self.height):
				if self.previouslyDrawn[i][j]==-1:
					paint.eraseRect(i*self.cell_size-1,j*self.cell_size-1,self.cell_size+2,self.cell_size+2)
		for i in range(self.width):
			for j in range(self.height):
				if self.sugar[i][j]!=self.previouslyDrawn[i][j] :
					paint.setBrush(QtGui.QColor(200,188,0))
					paint.setPen(QtGui.QColor(200,188,0))
					paint.drawEllipse(i*self.cell_size+self.cell_size/2-self.sugar[i][j],j*self.cell_size+self.cell_size/2-self.sugar[i][j],2*self.sugar[i][j],2*self.sugar[i][j])
					self.previouslyDrawn[i][j]=self.sugar[i][j]
				if self.agents[i][j]!=None:
					paint.setBrush(self.agents[i][j].color)
					paint.setPen(self.agents[i][j].color)
					paint.drawEllipse(i*self.cell_size,j*self.cell_size,self.cell_size,self.cell_size)
					self.previouslyDrawn[i][j]=-1
		paint.end()
		self.pop_plot.update()
