import neuron, math, time, sys

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
						layers[l][n].w[j]-=lrate*data[i][0][j]*layers[l][n].d
				else:
					for j in range(nhnodes[l-1]):
						layers[l][n].w[j]-=lrate*layers[l-1][j].val*layers[l][n].d
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
