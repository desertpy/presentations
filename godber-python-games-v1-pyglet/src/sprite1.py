import pyglet

window = pyglet.window.Window()

ball_image = pyglet.resource.image('ball.png')
ball = pyglet.sprite.Sprite(ball_image, x=50, y=50)

@window.event
def on_draw():
    ball.draw()

pyglet.app.run()
