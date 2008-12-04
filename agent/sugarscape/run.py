import sys
from world import world
from agent import agent
import random
from PyQt4 import QtGui, QtCore
from map import map

app = QtGui.QApplication(sys.argv)
inname = sys.argv[1]

mp = map(inname)

wrld = world(mp)
for i in range(mp.mwidth*mp.mheight/8):
	agent(wrld,i)
wrld.show()
sys.exit(app.exec_())
