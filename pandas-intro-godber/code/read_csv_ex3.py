#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt

phxtemps2 = pd.read_csv('phx-temps.csv', index_col=0,
                        names=['highs', 'lows'],
                        parse_dates=True)
phxtemps2.plot()
plt.savefig('phxtemps2-all.png')

# Lets see 2012
phxtemps2['20120101':'20121231'].plot()
plt.savefig('phxtemps2-2012.png')

# How about just the difference between high and low?
phxtemps2['diff'] = phxtemps2.highs - phxtemps2.lows
phxtemps2['20120101':'20121231'].plot()
plt.savefig('phxtemps2-2012-diff.png')
