import pyglet

window = pyglet.window.Window()
window.push_handlers(pyglet.window.event.WindowEventLogger())

@window.event
def on_draw():
    window.clear()

pyglet.app.run()
