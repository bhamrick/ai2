class map:
	def __init__(self,filename=None):
		self.seasons=[]
		if filename != None:
			fin = open(filename,"r")
			numseasons = int(fin.readline())
			self.numseasons = numseasons
			self.mwidth, self.mheight = fin.readline().split()
			self.mwidth = int(self.mwidth)
			self.mheight= int(self.mheight)
			for i in range(numseasons):
				length = int(fin.readline())
				cap = []
				for x in range(self.mwidth):
					cap.append([])
					for y in range(self.mheight):
						cap[x].append(0)
				for y in range(self.mheight):
					line = fin.readline()
					for x in range(self.mwidth):
						cap[x][y]=ord(line[x])-ord('0')
				self.seasons.append([length,cap])
		else:
			self.mwidth, self.mheight = 50, 50
			self.numseasons = 1
			for i in range(self.numseasons):
				length = 50
				cap = []
				for x in range(self.mwidth):
					cap.append([])
					for y in range(self.mheight):
						cap[x].append(0)
				self.seasons.append([length,cap])
		self.current_season = 0
		self.counter = 0
	def new(self):
		self.mwidth, self.mheight = 50, 50
		self.numseasons = 1
		self.seasons=[]
		for i in range(self.numseasons):
			length = 50
			cap = []
			for x in range(self.mwidth):
				cap.append([])
				for y in range(self.mheight):
					cap[x].append(0)
			self.seasons.append([length,cap])
		self.current_season = 0
		self.counter = 0
	def write(self,filename):
		fout = open(filename,"w")
		fout.write(str(self.numseasons) + "\n" + str(self.mwidth) + " " + str(self.mheight) + "\n")
		for i in range(self.numseasons):
			fout.write(str(self.seasons[i][0])+"\n")
			for y in range(self.mheight):
				for x in range(self.mwidth):
					fout.write(str(self.seasons[i][1][x][y]))
				fout.write("\n")
		fout.close()
	def read(self,filename):
		self.seasons=[]
		fin = open(filename,"r")
		numseasons = int(fin.readline())
		self.numseasons = numseasons
		self.mwidth, self.mheight = fin.readline().split()
		self.mwidth = int(self.mwidth)
		self.mheight= int(self.mheight)
		for i in range(numseasons):
			length = int(fin.readline())
			cap = []
			for x in range(self.mwidth):
				cap.append([])
				for y in range(self.mheight):
					cap[x].append(0)
			for y in range(self.mheight):
				line = fin.readline()
				for x in range(self.mwidth):
					cap[x][y]=ord(line[x])-ord('0')
			self.seasons.append([length,cap])
		self.current_season = 0
		self.counter = 0
	def allocate(self,arr):
		for i in range(self.numseasons):
			length = 50
			cap = []
			for x in range(self.mwidth):
				cap.append([])
				for y in range(self.mheight):
					cap[x].append(0)
			arr.append([length,cap])
	def setNumseasons(self,numseasons):
		oldnumseasons = self.numseasons
		self.numseasons = numseasons
		if numseasons < oldnumseasons:
			self.seasons = self.seasons[:numseasons]
		else:
			for i in range(numseasons-oldnumseasons):
				length = 50
				cap = []
				for x in range(self.mwidth):
					cap.append([])
					for y in range(self.mheight):
						cap[x].append(0)
				self.seasons.append([length,cap])
	def setDimensions(self,nwidth,nheight):
		oldwidth, oldheight = self.mwidth, self.mheight
		self.mwidth = nwidth
		self.mheight = nheight
		newseasons = []
		self.allocate(newseasons)
		for i in range(self.numseasons):
			for x in range(min(oldwidth,nwidth)):
				for y in range(min(oldheight,nheight)):
					newseasons[i][1][x][y]=self.seasons[i][1][x][y]
		self.seasons = newseasons
	def setWidth(self,wid):
		self.setDimensions(wid,self.mheight)
	def setHeight(self,hei):
		self.setDimensions(self.mwidth,hei)
	def setCap(self,season,x,y,val):
		self.seasons[season][1][x][y]=val
	def getCap(self,season,x,y):
		return self.seasons[season][1][x][y]
	def current(self):
		return self.seasons[self.current_season][1]
	def season(self,season):
		return self.seasons[season][1]
	def duration(self,season):
		return self.seasons[season][0]
	def getDuration(self,season):
		return self.seasons[season][0]
	def setDuration(self,season,val):
		self.seasons[season][0]=val
	def step(self):
		self.counter+=1
		if self.counter >= self.seasons[self.current_season][0]:
			self.counter = 0
			self.current_season += 1
			if self.current_season >= self.numseasons:
				self.current_season = 0
