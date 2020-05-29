import pyglet
from pyglet.window import key

def preload(image):
    img = pyglet.image.load('./res/'+image)
    return img

def load_high_score(file):

    with open(file, 'r') as f:

        score = f.read()

    return score

def save_high_score(file, scr):

    with open(file, 'w') as f:

        f.write(str(scr))


class GameObject:
    def __init__(self, pos_x, pos_y, sprite, health=None):
        if health is not None:
            self.health = health
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = 0
        self.vel_y = 0
        self.sprite = sprite
        self.sprite.x = self.pos_x = pos_x
        self.sprite.y = self.pos_y = pos_y



    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        self.pos_x += self.vel_x * dt
        self.pos_y += self.vel_y * dt
        self. sprite.x = self.pos_x
        self.sprite.y = self.pos_y

