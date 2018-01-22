import os
import math
from random import choice

import pyglet

window = pyglet.window.Window()

# Setup Background
ground_tiles = pyglet.resource.image('ground_tiles.png')
ground_grid = pyglet.image.ImageGrid(ground_tiles, 2, 6)
grass_img = ground_grid[8]
grass_tile_ids = (7, 8, 9, 10)

bg_batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)
characters = pyglet.graphics.OrderedGroup(3)

num_columns = int(math.ceil(window.width/grass_img.width))
num_rows = int(math.ceil(window.height/grass_img.height))

grass_sprites = []
for column in range(num_columns):
    for row in range(num_rows):
        x, y = column * 64, row * 64
        grass_sprites.append(pyglet.sprite.Sprite(
                ground_grid[choice(grass_tile_ids)], x, y,
                batch=bg_batch, group=background
            ))

rock_sprite = pyglet.sprite.Sprite(ground_grid[0], 2 * 64, 4 * 64,
    batch=bg_batch, group=foreground)
bush_sprite = pyglet.sprite.Sprite(ground_grid[1], 6 * 64, 1 * 64,
    batch=bg_batch, group=foreground)

creatures_tile = pyglet.resource.image('resources/creatures_tile.png')
creatures_grid = pyglet.image.ImageGrid(creatures_tile, 30, 4)
hero_sprite = pyglet.sprite.Sprite(img=creatures_grid[(20,3)], batch=bg_batch, group=characters)
hero_sprite.update(x=1 * 64, y=0 * 64, rotation=270.0, scale=2.0)
monster_sprite = pyglet.sprite.Sprite(img=creatures_grid[(12,1)], batch=bg_batch, group=characters)
monster_sprite.update(x=6 * 64, y=5 * 64, scale=2.0)


@window.event
def on_draw():
    window.clear()
    bg_batch.draw()

pyglet.app.run()
