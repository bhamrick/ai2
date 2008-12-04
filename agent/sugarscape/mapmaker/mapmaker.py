from math import *
from PyQt4 import QtGui, QtCore
from map import *
import sys, os, commands, copy
from PyQt4.QtCore import SIGNAL, SLOT

class maparea(QtGui.QWidget):
	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.move(0,0)
		self.map = map()
		self.curseason = 0
		self.currentBrush = 0
		self.currentTool = 'pencil'
		self.currentStyle = 'replace'
		self.x1 = -1
		self.x2 = -1
		self.y1 = -1
		self.y2 = -1
		self.selectionWidth = 0
		self.selectionHeight = 0
		self.selection = []
		self.setDimensions(50,50)
		self.emit(SIGNAL("seasonChanged(PyQt_PyObject)"),self.curseason)
		self.emit(SIGNAL("numseasonsChanged(PyQt_PyObject)"),self.map.numseasons)
	def usePencil(self):
		self.currentTool = 'pencil'
	def useRect(self):
		self.currentTool = 'rect'
	def useEllipse(self):
		self.currentTool = 'ellipse'
	def useReplace(self):
		self.currentStyle = 'replace'
	def useSelectRect(self):
		self.currentTool = 'selectRect'
	def useSelectEllipse(self):
		self.currentTool = 'selectEllipse'
	def usePaste(self):
		self.currentTool = 'paste'
	def useMinimum(self):
		self.currentStyle = 'minimum'
	def useMaximum(self):
		self.currentStyle = 'maximum'
	def selectAll(self):
		self.selectionWidth = self.mwidth
		self.selectionHeight = self.mheight
		self.selection = copy.deepcopy(self.map.season(self.curseason))
	def setDimensions(self,wid,hei):
		self.mwidth = wid
		self.mheight = hei
		self.map.setDimensions(wid,hei)
		self.setFixedSize(10*self.mwidth+1,10*self.mheight+1)
	def setWidth(self,width):
		self.setDimensions(width,self.mheight)
	def setHeight(self,height):
		self.setDimensions(self.mwidth,height)
	def new(self):
		self.map.new()
		self.setDimensions(self.map.mwidth,self.map.mheight)
	def open(self,filename):
		self.map.read(filename)
		self.setDimensions(self.map.mwidth,self.map.mheight)
	def write(self,filename):
		self.map.write(filename)
	def paintEvent(self,event):
		paint = QtGui.QPainter()
		paint.begin(self)
		paint.eraseRect(0,0,self.mwidth*10,self.mheight*10)
		paint.setPen(QtGui.QColor(0,0,0))
		for i in range(self.mwidth+1):
			paint.drawLine(10*i,0,10*i,self.mheight*10)
		for i in range(self.mheight+1):
			paint.drawLine(0,10*i,self.mwidth*10,10*i)
		cap = self.map.season(self.curseason)
		paint.setBrush(QtGui.QColor(200,188,0))
		paint.setPen(QtGui.QColor(200,188,0))
		for x in range(self.mwidth):
			for y in range(self.mheight):
				paint.drawEllipse(10*x+5-cap[x][y],10*y+5-cap[x][y],2*cap[x][y],2*cap[x][y])
		paint.setBrush(QtCore.Qt.NoBrush)
		blackpen = QtGui.QPen(QtCore.Qt.black)
		blackpen.setWidth(2)
		paint.setPen(blackpen)
		if self.x1 != -1 and self.x2 != -1 and self.y1 != -1 and self.y2 != -1:
			paint.drawRect(10*self.x1,10*self.y1,10*self.x2-10*self.x1,10*self.y2-10*self.y1)
			if self.currentTool == 'ellipse' or self.currentTool == 'selectEllipse':
				paint.setPen(QtCore.Qt.black)
				paint.drawEllipse(10*self.x1,10*self.y1,10*self.x2-10*self.x1,10*self.y2-10*self.y1)
		paint.end()
	def setSeason(self,season):
		if(self.curseason != season):
			self.curseason = season
			self.update()
			self.emit(SIGNAL("seasonChanged(PyQt_PyObject)"),season)
	def setNumseasons(self,numseasons):
		self.map.setNumseasons(numseasons)
	def setCurrentBrush(self,newbrush):
		self.currentBrush = newbrush
	def mousePressEvent(self,event):
		if event.button() == QtCore.Qt.LeftButton:
			if self.currentTool == 'pencil':
				x = event.x()/10
				y = event.y()/10
				x = max(0,x)
				y = max(0,y)
				x = min(x,self.mwidth-1)
				y = min(y,self.mheight-1)
				if self.currentStyle == 'replace':
					self.map.season(self.curseason)[x][y]=self.currentBrush
				if self.currentStyle == 'minimum':
					self.map.season(self.curseason)[x][y]=min(self.map.season(self.curseason)[x][y],self.currentBrush)
				if self.currentStyle == 'maximum':
					self.map.season(self.curseason)[x][y]=max(self.map.season(self.curseason)[x][y],self.currentBrush)
			elif self.currentTool == 'rect' or self.currentTool == 'selectRect':
				self.x1 = event.x()/10
				self.y1 = event.y()/10
				self.x2 = event.x()/10+1
				self.y2 = event.y()/10+1
			elif self.currentTool == 'ellipse' or self.currentTool == 'selectEllipse':
				self.x1 = event.x()/10
				self.y1 = event.y()/10
				self.x2 = event.x()/10+1
				self.y2 = event.y()/10+1
		self.update()
	def mouseMoveEvent(self,event):
		if event.buttons() == QtCore.Qt.LeftButton:
			if self.currentTool == 'pencil':
				x = event.x()/10
				y = event.y()/10
				x = max(0,x)
				y = max(0,y)
				x = min(x,self.mwidth-1)
				y = min(y,self.mheight-1)
				if self.currentStyle == 'replace':
					self.map.season(self.curseason)[x][y]=self.currentBrush
				if self.currentStyle == 'minimum':
					self.map.season(self.curseason)[x][y]=min(self.map.season(self.curseason)[x][y],self.currentBrush)
				if self.currentStyle == 'maximum':
					self.map.season(self.curseason)[x][y]=max(self.map.season(self.curseason)[x][y],self.currentBrush)
			elif self.currentTool == 'rect' or self.currentTool == 'selectRect':
				self.x2 = event.x()/10+1
				self.y2 = event.y()/10+1
			elif self.currentTool == 'ellipse' or self.currentTool == 'selectEllipse':
				self.x2 = event.x()/10+1
				self.y2 = event.y()/10+1
		self.update()
	def pointPaint(self,x,y,brush = -1):
		if brush == -1:
			brush = self.currentBrush
		if self.currentStyle == 'replace':
			self.map.season(self.curseason)[x][y]=brush
		if self.currentStyle == 'minimum':
			self.map.season(self.curseason)[x][y]=min(self.map.season(self.curseason)[x][y],brush)
		if self.currentStyle == 'maximum':
			self.map.season(self.curseason)[x][y]=max(self.map.season(self.curseason)[x][y],brush)
	def mouseReleaseEvent(self,event):
		if event.button() == QtCore.Qt.LeftButton:
			self.x2 = event.x()/10+1
			self.y2 = event.y()/10+1
			self.x1 = max(0,self.x1)
			self.y1 = max(0,self.y1)
			self.x1 = min(self.x1,self.mwidth-1)
			self.y1 = min(self.y1,self.mheight-1)
			self.x2 = max(0,self.x2)
			self.y2 = max(0,self.y2)
			self.x2 = min(self.x2,self.mwidth)
			self.y2 = min(self.y2,self.mheight)
			if self.currentTool == 'rect':
				for x in range(self.x1,self.x2):
					for y in range(self.y1,self.y2):
						self.pointPaint(x,y)
			elif self.currentTool == 'ellipse':
				cx = (self.x1 + self.x2-1)/2.0
				cy = (self.y1 + self.y2-1)/2.0
				a = abs(self.x1-cx)
				b = abs(self.y1-cy)
				if a != 0 and b != 0:
					for x in range(self.x1,self.x2):
						for y in range(self.y1,self.y2):
							if (((x-cx)/a)**2 + ((y-cy)/b)**2)**0.5 <= 1:
								self.pointPaint(x,y)
			elif self.currentTool == 'selectRect':
				self.selectionWidth = self.x2 - self.x1
				self.selectionHeight = self.y2 - self.y1
				self.selection = []
				for x in range(self.x1, self.x2):
					self.selection.append([])
					for y in range(self.y1,self.y2):
						self.selection[x-self.x1].append(self.map.season(self.curseason)[x][y])
			elif self.currentTool == 'selectEllipse':
				self.selectionWidth = self.x2 - self.x1
				self.selectionHeight = self.y2 - self.y1
				self.selection = []
				cx = (self.x1 + self.x2-1)/2.0
				cy = (self.y1 + self.y2-1)/2.0
				a = abs(self.x1-cx)
				b = abs(self.y1-cy)
				if a != 0 and b != 0:
					for x in range(self.x1,self.x2):
						self.selection.append([])
						for y in range(self.y1,self.y2):
							if (((x-cx)/a)**2 + ((y-cy)/b)**2)**0.5 <= 1:
								self.selection[x-self.x1].append(self.map.season(self.curseason)[x][y])
							else:
								self.selection[x-self.x1].append(-1)
			elif self.currentTool == 'paste':
				self.pasteSelection(event.x()/10,event.y()/10)
			self.x1 = self.x2 = self.y1 = self.y2 = -1
		self.update()
	def pasteSelection(self,x,y):
		for dx in range(self.selectionWidth):
			for dy in range(self.selectionHeight):
				if self.selection[dx][dy]!=-1 and x+dx < self.mwidth and y+dy < self.mheight:
					self.pointPaint(x+dx,y+dy,self.selection[dx][dy])
class mainwindow(QtGui.QMainWindow):
	def __init__(self,app,parent=None):
		QtGui.QMainWindow.__init__(self,parent)
		self.app = app
		self.filename = ""
		self.setFixedSize(800,600)
		self.initMenuBar()
		self.mainArea = QtGui.QWidget(self)
		self.mainArea.move(0,35)
		self.mainArea.setFixedSize(800,580)
		self.mapscrollarea = QtGui.QScrollArea(self.mainArea)
		self.mapscrollarea.setFixedSize(500,500)
		self.maparea=maparea(self.mapscrollarea)
		self.mapscrollarea.setWidget(self.maparea)
		self.setWindowTitle("Map Maker")
		self.initToolBar()
		self.newSlot()
	def open(self,filename):
		self.maparea.open(filename)
		self.maparea.update()
		self.setNumseasons(self.maparea.map.numseasons)
		self.setSeason(0)
	def setNumseasons(self,numseasons):
		numseasons = int(numseasons)
		self.seasonComboBox.clear()
		for i in range(numseasons):
			self.seasonComboBox.addItem("Season "+str(i),QtCore.QVariant(i))
		self.seasonComboBox.setCurrentIndex(0)
		self.maparea.setNumseasons(numseasons)
		self.updateFields()
		self.emit(SIGNAL("numseasonsChanged(PyQt_PyObject)"),numseasons)
	def setSeasonlength(self,length):
		length = int(length)
		self.maparea.map.setDuration(self.maparea.curseason,length)
	def updateNumseasons(self):
		self.setNumseasons(self.numseasonsBox.text())
	def updateSeasonlength(self):
		self.setSeasonlength(self.seasonlengthBox.text())
	def setSeason(self,season):
		self.maparea.setSeason(season)
		self.updateFields()
		self.emit(SIGNAL("seasonChanged(PyQt_PyObject)"),season)
	def initMenuBar(self):
		self.menuBar = QtGui.QMenuBar(self)
		self.fileMenu = self.menuBar.addMenu("File")
		self.setMenuBar(self.menuBar)
		self.newAction = self.fileMenu.addAction("New")
		self.openAction = self.fileMenu.addAction("Open")
		self.saveAction = self.fileMenu.addAction("Save")
		self.saveAsAction = self.fileMenu.addAction("Save as")
		self.fileMenu.addSeparator()
		self.quitAction = self.fileMenu.addAction("Quit")
		self.connect(self.newAction,SIGNAL("triggered()"),self.newSlot)
		self.connect(self.quitAction,SIGNAL("triggered()"),app,SLOT("quit()"))
		self.connect(self.openAction,SIGNAL("triggered()"),self.openSlot)
		self.connect(self.saveAction,SIGNAL("triggered()"),self.saveSlot)
		self.connect(self.saveAsAction,SIGNAL("triggered()"),self.saveAsSlot)
	def foodIcon(self,r):
		pixmap = QtGui.QPixmap(10,10)
		pixmap.fill(QtGui.QColor(0,0,0,0))
		painter = QtGui.QPainter()
		painter.begin(pixmap)
		painter.setPen(QtGui.QColor(200,188,0))
		painter.setBrush(QtGui.QColor(200,188,0))
		painter.drawEllipse(5-r,5-r,2*r,2*r)
		painter.end()
		return QtGui.QIcon(pixmap)
	def updateDimensions(self):
		self.maparea.setDimensions(int(self.widthBox.text()),int(self.heightBox.text()))
	def initToolBar(self):
		self.widthLabel = QtGui.QLabel("Width: ",self.mainArea)
		self.heightLabel = QtGui.QLabel("Height: ",self.mainArea)
		self.widthBox = QtGui.QLineEdit(self.mainArea)
		self.heightBox = QtGui.QLineEdit(self.mainArea)
		self.widthLabel.setFixedSize(40,30)
		self.widthBox.setFixedSize(60,22)
		self.heightLabel.setFixedSize(45,30)
		self.heightBox.setFixedSize(60,22)
		self.widthLabel.move(self.maparea.width()+10,20)
		self.widthBox.move(self.widthLabel.x()+self.widthLabel.width(),self.widthLabel.y())
		self.heightLabel.move(self.widthBox.x()+self.widthBox.width()+20,self.widthBox.y())
		self.heightBox.move(self.heightLabel.x()+self.heightLabel.width(),self.heightLabel.y())
		self.widthBox.setValidator(QtGui.QDoubleValidator(1,300,0,self.widthBox))
		self.heightBox.setValidator(QtGui.QDoubleValidator(1,300,0,self.heightBox))
		self.connect(self.widthBox,SIGNAL("returnPressed()"),self.updateDimensions)
		self.connect(self.heightBox,SIGNAL("returnPressed()"),self.updateDimensions)
		
		self.seasonComboBox = QtGui.QComboBox(self.mainArea)
		self.seasonComboBox.move(self.maparea.width()+10,80)
		self.seasonComboBox.setFixedSize(80,20)
		self.connect(self.seasonComboBox,SIGNAL("currentIndexChanged(int)"),self.setSeason)
		
		self.numseasonsLabel = QtGui.QLabel("Number of Seasons: ",self.mainArea)
		self.numseasonsLabel.move(self.maparea.width()+10,50)
		self.numseasonsLabel.setFixedSize(120,30)
		self.numseasonsBox = QtGui.QLineEdit(self.mainArea)
		self.numseasonsBox.setValidator(QtGui.QDoubleValidator(1,20,0,self.numseasonsBox))
		self.numseasonsBox.move(self.numseasonsLabel.x()+self.numseasonsLabel.width(),self.numseasonsLabel.y())
		self.connect(self.numseasonsBox,SIGNAL("returnPressed()"),self.updateNumseasons)
		
		self.seasonlengthLabel = QtGui.QLabel("Season Length: ",self.mainArea)
		self.seasonlengthLabel.move(self.maparea.width()+10,150)
		self.seasonlengthLabel.setFixedSize(120,20)
		self.seasonlengthBox = QtGui.QLineEdit(self.mainArea)
		self.seasonlengthBox.setValidator(QtGui.QDoubleValidator(1,1000,0,self.seasonlengthBox))
		self.seasonlengthBox.move(self.seasonlengthLabel.x() + self.seasonlengthLabel.width(),self.seasonlengthLabel.y())
		self.connect(self.seasonlengthBox,SIGNAL("returnPressed()"),self.updateSeasonlength)
		
		self.brushBar = QtGui.QButtonGroup(self.mainArea)
		for i in range(5):
			button = QtGui.QToolButton(self.mainArea)
			button.setIcon(self.foodIcon(i))
			button.setCheckable(True)
			if(i == 0):
				button.setChecked(True)
			button.setIconSize(QtCore.QSize(10,10))
			button.setFixedSize(20,20)
			button.move(self.maparea.width()+50+25*i,180)
			self.brushBar.addButton(button,i)
		self.connect(self.brushBar,SIGNAL("buttonClicked(int)"),self.maparea.setCurrentBrush)

		self.toolBar = QtGui.QButtonGroup(self.mainArea)
		self.pencilButton = QtGui.QToolButton(self.mainArea)
		self.pencilButton.setIcon(QtGui.QIcon('pencilIcon.gif'))
		self.pencilButton.setCheckable(True)
		self.pencilButton.setChecked(True)
		self.pencilButton.move(self.maparea.width()+10,210)
		self.pencilButton.setFixedSize(25,25)
		self.toolBar.addButton(self.pencilButton,0)

		self.rectButton = QtGui.QToolButton(self.mainArea)
		self.rectButton.setIcon(QtGui.QIcon('rectIcon.gif'))
		self.rectButton.setCheckable(True)
		self.rectButton.move(self.pencilButton.x() + self.pencilButton.width() + 5, self.pencilButton.y())
		self.rectButton.setFixedSize(25,25)
		self.toolBar.addButton(self.rectButton,1)

		self.ellipseButton = QtGui.QToolButton(self.mainArea)
		self.ellipseButton.setIcon(QtGui.QIcon('ellipseIcon.gif'))
		self.ellipseButton.setCheckable(True)
		self.ellipseButton.move(self.rectButton.x() + self.rectButton.width() + 5, self.pencilButton.y())
		self.ellipseButton.setFixedSize(25,25)
		self.toolBar.addButton(self.ellipseButton,2)

		self.selectRectButton = QtGui.QToolButton(self.mainArea)
		self.selectRectButton.setIcon(QtGui.QIcon('rectSelectIcon.gif'))
		self.selectRectButton.setCheckable(True)
		self.selectRectButton.move(self.ellipseButton.x() + self.ellipseButton.width() + 5, self.ellipseButton.y())
		self.selectRectButton.setFixedSize(25,25)
		self.toolBar.addButton(self.selectRectButton,3)

		self.selectEllipseButton = QtGui.QToolButton(self.mainArea)
		self.selectEllipseButton.setIcon(QtGui.QIcon('ellipseSelectIcon.gif'))
		self.selectEllipseButton.setCheckable(True)
		self.selectEllipseButton.move(self.selectRectButton.x() + self.selectRectButton.width() + 5, self.selectRectButton.y())
		self.selectEllipseButton.setFixedSize(25,25)
		self.toolBar.addButton(self.selectEllipseButton,4)

		self.pasteButton = QtGui.QToolButton(self.mainArea)
		self.pasteButton.setIcon(QtGui.QIcon('pasteIcon.gif'))
		self.pasteButton.setCheckable(True)
		self.pasteButton.move(self.selectEllipseButton.x() + self.selectEllipseButton.width() + 5, self.selectEllipseButton.y())
		self.pasteButton.setFixedSize(25,25)
		self.toolBar.addButton(self.pasteButton,5)
		self.connect(self.toolBar,SIGNAL("buttonClicked(int)"),self.newTool)

		self.styleBar = QtGui.QButtonGroup(self.mainArea)
		self.replaceButton = QtGui.QToolButton(self.mainArea)
		self.replaceButton.setIcon(QtGui.QIcon('replaceIcon.gif'))
		self.replaceButton.setCheckable(True)
		self.replaceButton.setChecked(True)
		self.replaceButton.move(self.maparea.width()+10,240)
		self.replaceButton.setFixedSize(25,25)
		self.styleBar.addButton(self.replaceButton,0)

		self.minimumButton = QtGui.QToolButton(self.mainArea)
		self.minimumButton.setIcon(QtGui.QIcon('minimumIcon.gif'))
		self.minimumButton.setCheckable(True)
		self.minimumButton.move(self.replaceButton.width()+self.replaceButton.x() + 5, self.replaceButton.y())
		self.minimumButton.setFixedSize(25,25)
		self.styleBar.addButton(self.minimumButton,1)

		self.maximumButton = QtGui.QToolButton(self.mainArea)
		self.maximumButton.setIcon(QtGui.QIcon('maximumIcon.gif'))
		self.maximumButton.setCheckable(True)
		self.maximumButton.move(self.minimumButton.width() + self.minimumButton.x() + 5, self.minimumButton.y())
		self.maximumButton.setFixedSize(25,25)
		self.styleBar.addButton(self.maximumButton,2)
		self.connect(self.styleBar,SIGNAL("buttonClicked(int)"),self.newStyle)

		self.selectAllButton=QtGui.QToolButton(self.mainArea)
		self.selectAllButton.setText('Select All')
		self.selectAllButton.move(self.maparea.width()+10,270)
		self.connect(self.selectAllButton,SIGNAL("clicked()"),self.maparea.selectAll)
		self.updateFields()
	def newTool(self,id):
		if id == 0:
			self.maparea.usePencil()
		elif id == 1:
			self.maparea.useRect()
		elif id == 2:
			self.maparea.useEllipse()
		elif id == 3:
			self.maparea.useSelectRect()
		elif id == 4:
			self.maparea.useSelectEllipse()
		elif id == 5:
			self.maparea.usePaste()
	def newStyle(self,id):
		if id == 0:
			self.maparea.useReplace()
		elif id == 1:
			self.maparea.useMinimum()
		elif id == 2:
			self.maparea.useMaximum()
	def openSlot(self):
		filename = QtGui.QFileDialog.getOpenFileName(None,"Open File","","All files (*.*)")
		if filename != "":
			self.filename = filename
			self.open(filename)
		self.updateTitle()
		self.update()
	def saveAsSlot(self):
		filename = QtGui.QFileDialog.getSaveFileName(None,"Save File","","All files (*.*)")
		if filename != "":
			self.filename = filename
			self.maparea.write(filename)
		self.updateTitle()
	def saveSlot(self):
		if self.filename == "":
			filename = QtGui.QFileDialog.getSaveFileName(None,"Save File","","All files (*.*)")
			if filename != "":
				self.filename = filename
				self.maparea.write(filename)
		else:
			self.maparea.write(self.filename)
	def updateTitle(self):
		if self.filename != "":
			self.setWindowTitle("Map Maker - " + self.filename)
		else:
			self.setWindowTitle("Map Maker - Untitled")
		self.update()
	def newSlot(self):
		self.filename = ""
		self.maparea.new()
		self.setNumseasons(self.maparea.map.numseasons)
		self.setSeason(0)
		self.updateTitle()
		self.update()
	def updateFields(self):
		self.updateTitle()
		self.numseasonsBox.setText(str(self.maparea.map.numseasons))
		self.seasonlengthBox.setText(str(self.maparea.map.getDuration(self.maparea.curseason)))
		self.widthBox.setText(str(self.maparea.map.mwidth))
		self.heightBox.setText(str(self.maparea.map.mheight))

app = QtGui.QApplication(sys.argv)
mwin = mainwindow(app=app)
mwin.show()
sys.exit(app.exec_())
