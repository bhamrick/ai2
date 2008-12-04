import math
from PyQt4 import QtGui, QtCore

class linegraph(QtGui.QWidget):
	def __init__(self,numitems,numseries=1,parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.resize(500,500)
		self.numitems=numitems
		self.numseries=numseries
		self.series=[]
		self.series_labels=[]
		self.series_pen=[]
		self.count=0
		for i in range(numseries):
			self.series.append([])
			self.series_labels.append('Series ' + str(i))
			self.series_pen.append(QtGui.QPen(QtGui.QColor(0,0,0)))
	def setcolor(self,series,color):
		self.series_pen[series]=QtGui.QPen(color)
	def addval(self,series,val):
		self.series[series].append(val)
		if len(self.series[series]) > self.numitems:
			self.series[series].pop(0)
	def inc(self):
		self.count+=1
	def paintEvent(self,event):
		paint=QtGui.QPainter()
		paint.begin(self)
		paint.setPen(QtGui.QColor(0,0,0))
		paint.drawText(3,13,str(self.count))
		paint.drawLine(0,0,0,self.height())
		paint.drawLine(0,self.height(),self.width(),self.height())
		for series in range(self.numseries):
			paint.setPen(self.series_pen[series])
			if len(self.series[series])>0:
				paint.drawText(3,23+10*series,str(self.series[series][-1]))
				path = QtGui.QPainterPath(QtCore.QPointF(1,self.height()-self.series[series][0]))
				for i in range(1,len(self.series[series])):
					path.lineTo(int(i*self.width()/len(self.series[series])),self.height()-int(self.series[series][i]))
				paint.drawPath(path)
		paint.end()
