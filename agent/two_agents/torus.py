import sys
import math
import random
from world import world
from herbivore import herbivore
from carnivore import carnivore
from PyQt4 import QtGui, QtCore

app = QtGui.QApplication(sys.argv)
wrld = world(800,600,'toroidal')
for i in range(100):
	wrld.agents.append(herbivore(wrld))
for i in range(30):
	wrld.agents.append(carnivore(wrld))
wrld.show()
sys.exit(app.exec_())
