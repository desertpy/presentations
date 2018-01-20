import os
import math
from random import choice

import pyglet

window = pyglet.window.Window()

ground_tiles = pyglet.resource.image('ground_tiles.png')
ground_grid = pyglet.image.ImageGrid(ground_tiles, 2, 6)
grass_tile_ids = (7, 8, 9, 10)
bg_batch = pyglet.graphics.Batch()

num_columns = int(math.ceil(window.width/ground_grid[0].width))
num_rows = int(math.ceil(window.height/ground_grid[0].height))
grass_sprites = []
for column in range(num_columns):
    for row in range(num_rows):
        x, y = column * 64, row * 64
        grass_sprites.append(pyglet.sprite.Sprite(
            ground_grid[choice(grass_tile_ids)], x, y, batch=bg_batch))

@window.event
def on_draw():
    window.clear()
    bg_batch.draw()

pyglet.app.run()
