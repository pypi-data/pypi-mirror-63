from .observable_linear import *
from .pooling import *

import chainer
import chainer.functions as F
import chainer.links as L

class Conv2D_BN(chainer.Chain):
	def __init__(self, insize, outsize, ksize,
		stride=1, pad=0,
		activation=F.relu,
		nobias=True,
		use_gamma=False,
		eps=2e-5):

		super(Conv2D_BN, self).__init__()
		assert callable(activation)

		with self.init_scope():
			self.conv = L.Convolution2D(insize, outsize,
				ksize=ksize, stride=stride, pad=pad, nobias=nobias)
			self.bn = L.BatchNormalization(outsize,
				use_gamma=use_gamma, eps=eps)

		self.activation = activation

	def forward(self, x):
		x = self.conv(x)
		x = self.bn(x)
		return self.activation(x)
