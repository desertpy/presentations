#!/usr/bin/env python
import numpy as np

# np.zeros, np.ones
data0 = np.zeros((2, 4))
#array([[ 0.,  0.,  0.,  0.],
#       [ 0.,  0.,  0.,  0.]])
data1 = np.arange(100)
#array([  0, 1, 2, .. 99])
data = np.arange(20).reshape(4, 5)
#array([[ 0,  1,  2,  3,  4],
#       [ 5,  6,  7,  8,  9],
#       [10, 11, 12, 13, 14],
#       [15, 16, 17, 18, 19]])
