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

# Simple Column Manipulations
data2['E'] = data2['B'] + 5 * data2['C']
#                    A         B         C         D         E
# 2013-06-26  0.014781  0.929893  0.402966  0.014548  2.944723
# 2013-06-27  0.968832  0.015926  0.976208  0.507152  4.896967
# 2013-06-28  0.381733  0.916911  0.828290  0.678275  5.058361
# 2013-06-29  0.447551  0.066915  0.308007  0.426910  1.606950

# Deleting a Column
del data2['E']
#                    A         B         C         D
# 2013-06-26  0.538854  0.061999  0.099601  0.010284
# 2013-06-27  0.800049  0.978754  0.035285  0.383580
# 2013-06-28  0.761694  0.764043  0.136828  0.066216
# 2013-06-29  0.129422  0.756846  0.931354  0.380510

# Column Access
# dict
data2['B']
# or attribute
data2.B

# Row Access
# by row label
data2.loc['20130627']
# by integer location
data2.iloc[1]

# For large DataFrames
data3 = pd.DataFrame(np.random.rand(400, 4))
data2.head()
data2.tail()
