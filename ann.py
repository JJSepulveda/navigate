################
## Artificial neuronal network
################

import numpy as np
import matplotlib.pyplot as plt


class neuronal_network(object):
	def __init__(self, inputs, hidden, outputs):
		D = inputs
		M = hidden
		K = outputs
		self.W1 = np.random.randn(D, M)
		self.b1 = np.random.randn(M)
		self.W2 = np.random.randn(M, K)
		self.b2 = np.random.randn(K)
		self.outputs = K

	def sigmoid(self, a):
		return 1 / (1 + np.exp(-a))

	def softmax(self, A):
		expA = np.exp(A)
		Y = expA / expA.sum(keepdims=True)
		return Y
	def tanh(self, a):
		expa = np.exp(a)
		expminusa = np.exp(-a)
		Y = (expa - expminusa) / (expa + expminusa)
		return Y
	def get_weights_and_bias(self):
		flat_weights = np.append(self.W1.reshape(-1), self.b1.reshape(-1))
		flat_weights = np.append(flat_weights, self.W2.reshape(-1))
		flat_weights = np.append(flat_weights, self.b2.reshape(-1))
		return flat_weights
	def set_weights_and_bias(self,buff):
		index_w1 = self.W1.size
		W1 = buff[0:index_w1]
		index_b1 = index_w1 + self.b1.size
		b1 = buff[index_w1:index_b1]
		index_w2 = index_b1+ self.W2.size
		W2 = buff[index_b1:index_w2]
		index_b2 = index_w2 +self.b2.size
		b2 = buff[index_w2:index_b2]

		#print("indices: W1: {}, b1: {}, W2: {}, b2: {}".format(index_w1,index_b1,index_w2,index_b2))

		#print("shape W1: {}".format(W1.shape))
		#print("shape b1: {}".format(b1.shape))
		#print("shape W2: {}".format(W2.shape))
		#print("shape b2: {}".format(b2.shape))

		self.W1 = W1.reshape(self.W1.shape)
		self.b1 = b1.reshape(self.b1.shape)
		self.W2 = W2.reshape(self.W2.shape)
		self.b2 = b2.reshape(self.b2.shape)

	def predict(self, X):

		if(type(X) is list):
			X = np.array(X)

		Z = self.tanh(X.dot(self.W1) + self.b1)
		A = Z.dot(self.W2) + self.b2

		if(self.outputs == 1):
			Y = self.sigmoid(A)
		else:
			Y = self.softmax(A)

		#print(self.W1.shape)
		#print(self.W1)
		#print(self.b1.shape)
		#print(self.b1)
		#print(self.W2.shape)
		#print(self.W2)
		#print(self.b2.shape)
		#print(self.b2)
		#print(type(self.b2[0]))
		return Y

if(__name__ == '__main__'):
	ann = neuronal_network(4,4,1)
	inputs = np.array([0.8, 0.4, 0.8, 0.4])
	p = ann.predict(inputs)

	flat = ann.get_weights_and_bias()
	#print(flat)
	#print(flat.shape)

	ann.set_weights_and_bias(flat)