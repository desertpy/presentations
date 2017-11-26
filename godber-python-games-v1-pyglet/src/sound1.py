import pyglet

window = pyglet.window.Window()
sound = pyglet.resource.media('resources/bullet.wav', streaming=False)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        sound.play()

@window.event
def on_draw():
    window.clear()

pyglet.app.run()
