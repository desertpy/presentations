#!/usr/bin/env python
import pyglet

window = pyglet.window.Window()
image = pyglet.resource.image('ground_tiles.png')

@window.event
def on_draw():
    window.clear()
    image.blit(0, 0)

pyglet.app.run()
