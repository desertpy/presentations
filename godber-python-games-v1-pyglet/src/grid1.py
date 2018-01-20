import os
import pyglet
window = pyglet.window.Window()

ground_tiles = pyglet.resource.image('ground_tiles.png')
# describe the ImageGrid layout is 2 x 6
ground_grid = pyglet.image.ImageGrid(ground_tiles, 2, 6)
# use integers to index into the grid from the bottom left
grass_spite = pyglet.sprite.Sprite(img=ground_grid[8])

@window.event
def on_draw():
    window.clear()
    grass_spite.draw()

pyglet.app.run()
