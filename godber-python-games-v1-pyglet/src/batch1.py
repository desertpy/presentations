import pyglet

window = pyglet.window.Window()

ball_image = pyglet.resource.image('ball.png')
batch = pyglet.graphics.Batch()

ball_sprites = []
for i in range(100):
    x, y = i * 10, (i * 10 % window.height)
    ball_sprites.append(pyglet.sprite.Sprite(ball_image, x, y, batch=batch))

@window.event
def on_draw():
    batch.draw()

pyglet.app.run()
