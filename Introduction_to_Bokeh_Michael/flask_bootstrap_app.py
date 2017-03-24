from flask import Flask, render_template
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.embed import components
import pandas as pd
import numpy as np

app = Flask(__name__)

def plot_maker(n):
    p = figure(title='bob'+str(n),
               tools='hover,pan,reset',
               width=400, height=300,
               responsive=True)
    dt = pd.DataFrame(np.random.randint(0, 100, size=(100, 2)),
                      columns=list('XY'))
    dt = ColumnDataSource(data=dt)
    p.scatter(x='X', y='Y', source=dt)
    return components(p)


@app.route("/", methods=['GET'])
def grid_plots():
    groups = []
    k = -1
    for i in range(12):
        if i % 4 == 0:
            groups.append({'name': 'Group' + str(int(i/4)),
                          'plots': []})
            k += 1
        script, div = plot_maker(i)
        plot = script+div
        groups[k]['plots'].append(plot)
    grid = render_template('index.html', groups=groups)
    return grid


if __name__ == '__main__':
    app.run(port=8889)

