from flask import Flask, render_template

from tornado.ioloop import IOLoop
from collections import deque

from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.embed import autoload_server
from bokeh.resources import CDN, INLINE
from bokeh.layouts import column
from bokeh.util.browser import view
from bokeh.models.tools import HoverTool
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.server.server import Server
import threading
from date_range_slider import generate_date_range_slider
import bitcoin_price as bp
from datetime import datetime, timedelta

app = Flask(__name__)

def modify_doc(doc):
    days_back = 180
    end = datetime.now()
    start = end - timedelta(days=days_back)
    df = bp.bitcoin_price_history(datetime.strftime(start, '%Y-%m-%d'),
                                  datetime.strftime(end, '%Y-%m-%d'))
    df['label'] = df['date'].apply(lambda s: s.strftime('%Y/%m/%d'))
    source = ColumnDataSource(data=df)

    history = figure(width=800, height=400,
                     title='Historical Price last {} days'.format(
                                                           days_back),
                     tools='hover,reset,save,box_zoom,wheel_zoom',
                     x_axis_type='datetime', responsive=True)
    history.line('date', 'price', color='blue', line_width=3,
                 source=source, alpha=0.6)
    history.circle('date', 'price', color='green', size=8,
                   source=source, name='points', line_color='navy')

    hover = history.select(HoverTool)
    hover.names = ['points']
    hover.tooltips =[('Price (USD)', '@price{0.00}'),
                     ('Date', '@label')]
    history.xaxis.axis_label = 'Date'
    history.yaxis.axis_label = 'Price (USD)'

    # Set up current data refresh
    cur_dt, cur_prc = bp.bitcoin_current_price()
    x = deque([cur_dt], maxlen=60)
    y = deque([cur_prc], maxlen=60)
    label = deque([cur_dt.strftime('%Y/%m/%d %H:%M')],
                  maxlen=60)
    cur_source = ColumnDataSource(data=dict(date=x,
                                            price=y,
                                            label=label))
    current = figure(width=800, height=400,
                     title='Current Price Tracking: ${} {}'.format(
                                                    round(cur_prc, 2),
                                                    label[0]),
                     tools='hover,reset,save,box_zoom,wheel_zoom',
                     x_axis_type='datetime', responsive=True)
    current.line('date', 'price', color='blue', line_width=3,
                 source=cur_source, alpha=0.6)
    current.circle('date', 'price', color='purple', size=8,
                   source=cur_source, name='points', line_color='navy')
    hover = current.select(HoverTool)
    hover.names = ['points']
    hover.tooltips = [('Price (USD)', '@price{0.00}'),
                      ('Date', '@label')]
    history.xaxis.axis_label = 'Date'
    history.yaxis.axis_label = 'Price (USD)'
    current.xaxis.axis_label = 'Date'
    current.yaxis.axis_label = 'Price (USD)'

    div, range_slider = generate_date_range_slider(days=days_back)

    outline = column(current, div, range_slider, history, responsive=True)

    def date_range_callback(attr, old, new):
        # add delta of 1 day for conversion discrepancy with local time
        delta = timedelta(days=1)
        start = datetime.fromtimestamp(new[0]). \
                replace(hour=0, minute=0,
                        second=0, microsecond=0) + delta
        end = datetime.fromtimestamp(new[1]). \
                replace(hour=23, minute=59,
                        second=59, microsecond=999999) + delta
        new_df = df[(df['date'] >= start) & (df['date'] < end)]
        source.data = source.from_df(new_df)

    def trigger_current_update():
        print('triggered')
        n_cur_dt, n_cur_prc = bp.bitcoin_current_price()
        n_label = n_cur_dt.strftime('%Y/%m/%d %H:%M')
        current.title.text = 'Current Price Tracking: ${} {}'.format(
                                                         round(n_cur_prc, 2),
                                                         n_label)
        x.append(n_cur_dt)
        y.append(n_cur_prc)
        label.append(n_label)
        # convert to lists because after a deque of size 2
        # data source mysteriously fails to update...
        cur_source.data = dict(date=list(x),
                               price=list(y),
                               label=list(label))
        print(n_cur_dt, n_cur_prc)

    range_slider.on_change('range', date_range_callback)
    doc.add_periodic_callback(trigger_current_update,
                              period_milliseconds=60000)
    doc.add_root(outline)


def start_ioloop(ioloop):
    ioloop.add_callback(view, "http://localhost:8080/")
    ioloop.start()


@app.route("/", methods=['GET'])
def hello_world():
    script = autoload_server(model=None,
                             url='http://localhost:5006/bkapp')
    return render_template("embed1.html", script=script,
                           resources=CDN.render())


if __name__ == '__main__':
    bokeh_app = Application(FunctionHandler(modify_doc))
    io_loop = IOLoop.current()
    server = Server({'/bkapp': bokeh_app}, io_loop=io_loop,
                    allow_websocket_origin=["localhost:8080"])
    server.start()

    t = threading.Thread(target=start_ioloop, args=(io_loop,))
    t.daemon = True
    t.start()
    try:
        app.run(port=8080)
    except KeyboardInterrupt:
        io_loop.stop()
