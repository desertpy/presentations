#!/usr/bin/env python
import numpy as np

data = np.arange(20).reshape(4, 5)
#array([[ 0,  1,  2,  3,  4],
#       [ 5,  6,  7,  8,  9],
#       [10, 11, 12, 13, 14],
#       [15, 16, 17, 18, 19]])
data.dtype
#dtype('int64')
result = data * 20.5
#array([[   0. ,   20.5,   41. ,   61.5,   82. ],
#      ...
#       [ 307.5,  328. ,  348.5,  369. ,  389.5]])
result.dtype
#dtype('float64')
