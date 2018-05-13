from builtins import object
import numpy as np

from cs231n.layers import *
from cs231n.fast_layers import *
from cs231n.layer_utils import *


class ThreeLayerConvNet(object):
    """
    A three-layer convolutional network with the following architecture:

    conv - relu - 2x2 max pool - affine - relu - affine - softmax

    The network operates on minibatches of data that have shape (N, C, H, W)
    consisting of N images, each with height H and width W and with C input
    channels.
    """

    def __init__(self, input_dim=(3, 32, 32), num_filters=32, filter_size=7,
                 hidden_dim=100, num_classes=10, weight_scale=1e-3, reg=0.0,
                 dtype=np.float32):
        """
        Initialize a new network.

        Inputs:
        - input_dim: Tuple (C, H, W) giving size of input data
        - num_filters: Number of filters to use in the convolutional layer
        - filter_size: Size of filters to use in the convolutional layer
        - hidden_dim: Number of units to use in the fully-connected hidden layer
        - num_classes: Number of scores to produce from the final affine layer.
        - weight_scale: Scalar giving standard deviation for random initialization
          of weights.
        - reg: Scalar giving L2 regularization strength
        - dtype: numpy datatype to use for computation.
        """
        self.params = {}
        self.reg = reg
        self.dtype = dtype

        C, H, W = input_dim
        F = num_filters
        HH = filter_size
        hdn = 100
        cls = 10

        self.params['W1'] = np.random.randn(F,C,HH,HH) * weight_scale
        self.params['b1'] = np.zeros(F)
        self.params['W2'] = np.random.randn(F*int(H/2)**2, hdn) * weight_scale
        self.params['b2'] = np.zeros(hdn)
        self.params['W3'] = np.random.randn(hdn, cls) * weight_scale
        self.params['b3'] = np.zeros(cls)

        for k, v in self.params.items():
            self.params[k] = v.astype(dtype)


    def loss(self, X, y=None):
        """
        Evaluate loss and gradient for the three-layer convolutional network.

        Input / output: Same API as TwoLayerNet in fc_net.py.
        """
        W1, b1 = self.params['W1'], self.params['b1']
        W2, b2 = self.params['W2'], self.params['b2']
        W3, b3 = self.params['W3'], self.params['b3']

        # pass conv_param to the forward pass for the convolutional layer
        filter_size = W1.shape[2]
        conv_param = {'stride': 1, 'pad': (filter_size - 1) // 2}

        # pass pool_param to the forward pass for the max-pooling layer
        pool_param = {'pool_height': 2, 'pool_width': 2, 'stride': 2}

        scores = None

        out, cache_conv = conv_relu_pool_forward(X, W1, b1, conv_param, pool_param)
        out, cache_aff1 = affine_relu_forward(out, W2, b2)
        scores, cache_aff2 = affine_forward(out, W3, b3)

        if y is None:
            return scores

        loss, grads = 0, {}

        loss, dout = softmax_loss(scores, y)
        loss += 0.5*self.reg*(np.sum(self.params['W1']**2)+np.sum(self.params['W2']**2)+np.sum(self.params['W3']**2))

        dout, grads['W3'], grads['b3'] = affine_backward(dout, cache_aff2)
        dout, grads['W2'], grads['b2'] = affine_relu_backward(dout, cache_aff1)
        dout, grads['W1'], grads['b1'] = conv_relu_pool_backward(dout, cache_conv)

        grads['W3'] += self.reg * self.params['W3']
        grads['W2'] += self.reg * self.params['W2']
        grads['W1'] += self.reg * self.params['W1']

        return loss, grads
