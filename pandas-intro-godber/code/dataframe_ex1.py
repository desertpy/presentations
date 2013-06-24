#!/usr/bin/env python
import pandas as pd
import numpy as np

# Simple DataFrame
data1 = pd.DataFrame(np.random.rand(4, 4))
#          0         1         2         3
# 0  0.748663  0.119829  0.382114  0.375031
# 1  0.549362  0.409125  0.336181  0.870665
# 2  0.102960  0.539968  0.356454  0.661136
# 3  0.233307  0.338176  0.577226  0.966152

# Custom Index and Column Names
dates = pd.date_range('20130626', periods=4)
data2 = pd.DataFrame(np.random.rand(4, 4), index=dates, columns=list('ABCD'))
#                    A         B         C         D
# 2013-06-26  0.538854  0.061999  0.099601  0.010284
# 2013-06-27  0.800049  0.978754  0.035285  0.383580
# 2013-06-28  0.761694  0.764043  0.136828  0.066216
# 2013-06-29  0.129422  0.756846  0.931354  0.380510
