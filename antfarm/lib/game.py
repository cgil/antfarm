import pyglet
import pymunk
from pymunk.pyglet_util import draw as pymunk_draw
from pyglet.window import key

from antfarm.lib import constants
from antfarm.lib.ant import Ant
from antfarm.lib.opening import Opening


class Game(pyglet.window.Window):

    def __init__(self):
        super(Game, self).__init__(width=constants.WINDOW_WIDTH, height=constants.WINDOW_HEIGHT)
        self.keys = {}
        self.space = pymunk.Space()
        self.batch = pyglet.graphics.Batch()
        self.tunnel_batch = pyglet.graphics.Batch()
        self.ant_image = pyglet.resource.image('ant.png')
        self.opening_image = pyglet.resource.image('ground.png')
        self.ants = []
        self.grid = []
        self.tunnel_openings = []

        self.space.add_collision_handler(
            constants.ANT_COLLISION_TYPE,
            constants.OPENING_COLLISION_TYPE,
            pre_solve=Game.pre_solve_collision,
            separate=Game.seperate_collision,
            # begin=Game.begin_collision
        )
        pyglet.gl.glClearColor(*constants.DEF_BKGDCOLOR)
        pyglet.clock.schedule(self.update)

    def add_to_tunnel(self, x, y):
        """Adds to the tunnel."""
        opening = Opening(
            self.tunnel_batch, self.space.static_body, self.opening_image, self.space,
            x, y
        )
        self.tunnel_openings.append(opening)

    def add_ant(self):
        """Add an ant to the game."""
        ant = Ant(batch=self.batch, img=self.ant_image, space=self.space)
        self.ants.append(ant)

    def on_draw(self):
        self.clear()
        pymunk_draw(self.tunnel_openings, self.tunnel_batch)
        self.tunnel_batch.draw()
        self.batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self.keys['up'] = True
        elif symbol == key.LEFT:
            self.keys['left'] = True
        elif symbol == key.RIGHT:
            self.keys['right'] = True
        elif symbol == key.DOWN:
            self.keys['down'] = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP:
            self.keys['up'] = False
        elif symbol == key.LEFT:
            self.keys['left'] = False
        elif symbol == key.RIGHT:
            self.keys['right'] = False
        elif symbol == key.DOWN:
            self.keys['down'] = False

    def update(self, dt):
        for ant in self.ants:
            ant.update(dt, self.keys)
        self.space.step(dt)
