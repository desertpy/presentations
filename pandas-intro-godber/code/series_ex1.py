#!/usr/bin/env python
import pandas as pd

# Simple Series
s1 = pd.Series([1, 2, 3, 4, 5])
# 0    1
# 1    2
# 2    3
# 3    4
# 4    5
# dtype: int64

# Operations
print s1 * 5
# 0     5
# 1    10
# 2    15
# 3    20
# 4    25
# dtype: int64

# Mixed type operations
print s1 * 5.0
# 0     5
# 1    10
# 2    15
# 3    20
# 4    25
# dtype: float64

# Custom Index
s2 = pd.Series([1, 2, 3, 4, 5], index=['a', 'b', 'c', 'd', 'e'])
# a    1
# b    2
# c    3
# d    4
# e    5
# dtype: int64

# Date Convenience Functions
dates = pd.date_range('20130626', periods=5)
# <class 'pandas.tseries.index.DatetimeIndex'>
# [2013-06-26 00:00:00, ..., 2013-06-30 00:00:00]
# Length: 5, Freq: D, Timezone: None

dates[0]
# <Timestamp: 2013-06-26 00:00:00>

# Datestamps as index
s3 = pd.Series([1, 2, 3, 4, 5], index=dates)
# 2013-06-26    1
# 2013-06-27    2
# 2013-06-28    3
# 2013-06-29    4
# 2013-06-30    5
# Freq: D, dtype: int64

# Selecting By Index
s3[0]
# 1
s3[1:3]
# 2013-06-27    2
# 2013-06-28    3
# Freq: D, dtype: int64

# Selecting by value
s3[s3 < 3]
# 2013-06-26    1
# 2013-06-27    2
# Freq: D, dtype: int64

# Selecting by Label (Date)
s3['20130626':'20130628']
# 2013-06-26    1
# 2013-06-27    2
# 2013-06-28    3
# Freq: D, dtype: int64
