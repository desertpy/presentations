import pyglet

window = pyglet.window.Window()
window.push_handlers(pyglet.window.event.WindowEventLogger())

@window.event
def on_key_press(symbol, modifiers):
    print('A key was pressed: Symbol: %s, Modifier: %s' % (symbol, modifiers))

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        print('The left mouse button was pressed.')

@window.event
def on_draw():
    window.clear()

pyglet.app.run()
