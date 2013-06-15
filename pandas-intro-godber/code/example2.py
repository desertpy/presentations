#!/usr/bin/env python

import pandas as pd

phxtemps = pd.read_csv('phx-temps.csv', index_col=0,
                       names=['highs', 'lows'],
                       parse_dates=True)
print "=" * 80
print phxtemps
print "=" * 80
print phxtemps.head()
print "=" * 80
