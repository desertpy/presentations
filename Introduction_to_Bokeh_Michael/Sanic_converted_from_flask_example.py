from sanic import Sanic
from sanic.response import html
from jinja2 import Template

import numpy as np
from tornado.ioloop import IOLoop

from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from bokeh.embed import autoload_server
from bokeh.layouts import column
from bokeh.util.browser import view
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
import threading


app = Sanic()


def modify_doc(doc):
    x = np.linspace(0, 10, 1000)
    y = np.log(x) * np.sin(x)

    source = ColumnDataSource(data=dict(x=x, y=y))

    plot = figure()
    plot.line('x', 'y', source=source)

    slider = Slider(start=1, end=10, value=1, step=0.1)

    def callback(attr, old, new):
        y = np.log(x) * np.sin(x*new)
        source.data = dict(x=x, y=y)
    slider.on_change('value', callback)

    doc.add_root(column(slider, plot))


def start_ioloop(ioloop):
    io_loop.add_callback(view, "http://localhost:8899/")
    io_loop.start()


@app.route("/", methods=['GET'])
async def test(request):
    script = autoload_server(model=None, url='http://localhost:5116/bkapp')
    with open("templates/embed.html") as tmp:
        templt = tmp.read()
    return html(Template(templt).render(script=script))


if __name__ == "__main__":
    bokeh_app = Application(FunctionHandler(modify_doc))
    io_loop = IOLoop.current()
    server = Server({'/bkapp': bokeh_app}, io_loop=io_loop, port=5116,
                    allow_websocket_origin=["localhost:8899"])
    server.start()

    t = threading.Thread(target=start_ioloop, args=(io_loop,))
    t.daemon = True
    t.start()
    try:
        app.run(port=8899)
    except KeyboardInterrupt:
        io_loop.stop()