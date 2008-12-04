import sys
import math
import random
from world import world
from herbivore import herbivore
from PyQt4 import QtGui, QtCore

app = QtGui.QApplication(sys.argv)
wrld = world(800,600,'toroidal')
for i in range(20):
	wrld.agents.append(herbivore(wrld))
wrld.show()
sys.exit(app.exec_())
