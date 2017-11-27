import pyglet

window = pyglet.window.Window()
sound = pyglet.resource.media('resources/bullet.wav', streaming=False)

creatures_tile = pyglet.resource.image('resources/creatures_tile.png')
creatures_grid = pyglet.image.ImageGrid(creatures_tile, 30, 4)

ground_tiles = pyglet.resource.image('ground_tiles.png')
ground_grid = pyglet.image.ImageGrid(ground_tiles, 2, 6)

hero = creatures_grid[(20,3)]

hero_sprite = pyglet.sprite.Sprite(img=hero)
hero_sprite.rotation = 270.0
hero_sprite.position = (window.width // 2, window.height // 2)
hero_sprite.scale = 3.0

@window.event
def on_draw():
    window.clear()
    hero_sprite.draw()


pyglet.app.run()
