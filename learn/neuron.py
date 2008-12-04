import random, math

class neuron:
	def __init__(self,nweights):
		self.bias = random.random()
		self.w = []
		for i in range(nweights):
			self.w.append(random.random())
		self.sigma = lambda u: 1/(1+math.e**(-u))
		self.val = 0
		self.d = 0
	def output(self,inputs):
		tot = self.bias
		for i in range(min(len(inputs),len(self.w))):
			tot += inputs[i]*self.w[i]
		self.val = self.sigma(tot)
		return self.val
