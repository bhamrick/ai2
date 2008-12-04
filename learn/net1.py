import neuron, math, time, sys, random

interactive = False
mu = 0.1

if len(sys.argv) < 2:
	print 'YOU FAIL'
	sys.exit(0)

if sys.argv[1] == '-i':
	interactive = True
	sys.argv.pop(1)

if len(sys.argv) < 2:
	print 'YOU FAIL'
	sys.exit(0)

fname = sys.argv[1]
fin = open(fname,"r");

inputs = int(fin.readline().split()[0])
outputs = int(fin.readline().split()[0])
hlayers = int(fin.readline().split()[0])
nhnodes = []

for i in range(hlayers):
	nhnodes.append(int(fin.readline().split()[0]))
nhnodes.append(outputs)

lrate = float(fin.readline().split()[0])
niter = int(fin.readline().split()[0])
ndata = int(fin.readline().split()[0])
data = []
for i in range(ndata):
	foo = fin.readline().split()
	for i in range(len(foo)):
		try:
			foo[i]=int(foo[i])
		except:
			pass
	data.append([foo[:inputs],foo[inputs:inputs+outputs]])

layers = []
for l in range(hlayers+1):
	arr = []
	for i in range(nhnodes[l]):
		if l == 0:
			arr.append(neuron.neuron(inputs))
		else:
			arr.append(neuron.neuron(nhnodes[l-1]))
	layers.append(arr)

if not interactive:
	start = time.time()
	sys.stdout.write('Learning...')
	sys.stdout.flush()
	for k in range(niter):
		for i in range(ndata):
			#Feed Forward
			indata = data[i][0]
	#		print indata
			for l in range(len(layers)):
				nextdata = []
				for n in range(nhnodes[l]):
					nextdata.append(layers[l][n].output(indata))
				indata = nextdata
			outdata = []
			for n in range(nhnodes[-1]):
				outdata.append(layers[-1][n].val)
	#		print 'Got',outdata,'Expected',data[i][1]
		
			#Back Propogate
			for n in range(nhnodes[-1]):
				layers[-1][n].d = layers[-1][n].val - data[i][1][n]
			for l in range(hlayers-1,-1,-1):
				for n in range(nhnodes[l]):
					layers[l][n].d = 0
					for j in range(nhnodes[l+1]):
						layers[l][n].d+=layers[l+1][j].w[n]*layers[l+1][j].d
					layers[l][n].d*=layers[l][n].val*(1-layers[l][n].val)
			for l in range(hlayers+1):
				for n in range(nhnodes[l]):
					if l == 0:
						for j in range(inputs):
							layers[l][n].pdelta=mu*layers[l][n].pdelta - (1-mu)*lrate*data[i][0][j]*layers[l][n].d
							layers[l][n].w[j]+=layers[l][n].pdelta
					else:
						for j in range(nhnodes[l-1]):
							layers[l][n].pdelta=mu*layers[l][n].pdelta - (1-mu)*lrate*layers[l-1][j].val*layers[l][n].d
							layers[l][n].w[j]+=layers[l][n].pdelta
	end = time.time()
	sys.stdout.write('Done in %f seconds!\n\n' % (float(end)-float(start)))
	sys.stdout.flush()
	
	while True:
		line = raw_input("Input: ")
		indata = line.split()
		for i in range(len(indata)):
			try:
				indata[i] = int(indata[i])
			except:
				pass
		indata = indata[:inputs]
		for l in range(len(layers)):
			nextdata = []
			for n in range(nhnodes[l]):
				nextdata.append(layers[l][n].output(indata))
			indata = nextdata
		outdata = []
		for n in range(nhnodes[-1]):
			outdata.append(layers[-1][n].val)
		print 'Output:',outdata
else:
	while True:
		try:
			#Generate data
			indata = []
			for i in range(inputs):
				indata.append(int(2*random.random()))
			#Feed Forward
			print 'Input:',indata
			for l in range(len(layers)):
				nextdata = []
				for n in range(nhnodes[l]):
					nextdata.append(layers[l][n].output(indata))
				indata = nextdata
			outdata = []
			for n in range(nhnodes[-1]):
				outdata.append(layers[-1][n].val)
			print 'Got',outdata
			expected = raw_input('Expected: ').split()
			for i in range(len(expected)):
				expected[i] = int(expected[i])
		
			#Back Propogate
			for n in range(nhnodes[-1]):
				layers[-1][n].d = layers[-1][n].val - expected[n]
			for l in range(hlayers-1,-1,-1):
				for n in range(nhnodes[l]):
					layers[l][n].d = 0
					for j in range(nhnodes[l+1]):
						layers[l][n].d+=layers[l+1][j].w[n]*layers[l+1][j].d
					layers[l][n].d*=layers[l][n].val*(1-layers[l][n].val)
			for l in range(hlayers+1):
				for n in range(nhnodes[l]):
					if l == 0:
						for j in range(inputs):
							layers[l][n].pdelta=mu*layers[l][n].pdelta - (1-mu)*lrate*data[i][0][j]*layers[l][n].d
							layers[l][n].w[j]+=layers[l][n].pdelta
					else:
						for j in range(nhnodes[l-1]):
							layers[l][n].pdelta=mu*layers[l][n].pdelta - (1-mu)*lrate*layers[l-1][j].val*layers[l][n].d
							layers[l][n].w[j]+=layers[l][n].pdelta
		except KeyboardInterrupt:
			sys.exit(0)
		except:
			pass
