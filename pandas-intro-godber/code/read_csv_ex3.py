#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt

phxtemps2 = pd.read_csv('phx-temps.csv', index_col=0,
                        names=['highs', 'lows'],
                        parse_dates=True)


