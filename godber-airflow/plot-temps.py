#!/usr/bin/env python

# /srv/airflow/.virtualenvs/mpl/bin/python

from sys import argv
from os.path import abspath, dirname

import pandas as pd
import matplotlib.pyplot as plt


def main(infile, ds):
    df = pd.read_csv(infile, delim_whitespace=True, usecols=[2, 17, 18],
                     names=['date', 'max_temp', 'min_temp'])

    df2 = df.set_index(pd.to_datetime(df.date, format='%Y%m%d'))

    df3 = df2.drop(['date'], axis=1)

    ax = df3.plot(figsize=(11, 8.5))
    fig = ax.get_figure()
    outfile = f"{dirname(abspath(infile))}/phx-temp-{ds}.png"
    print(f"Generating output to {outfile}")
    fig.savefig(outfile)


if __name__ == '__main__':
    if len(argv) < 3:
        print(f"{argv[0]} <infile> <datestamp>")
    else:
        main(argv[1], argv[2])
