import pyglet
import pymunk
from pymunk.pyglet_util import draw as pymunk_draw
from pyglet.window import key

from antfarm.lib import constants
from antfarm.lib.ant import Ant
from antfarm.lib.opening import Opening
from antfarm.lib.encasing import Encasing


class Game(pyglet.window.Window):

    def __init__(self):
        super(Game, self).__init__(width=constants.WINDOW_WIDTH, height=constants.WINDOW_HEIGHT)
        self.keys = {}
        self.space = pymunk.Space()
        # self.space.gravity = (0.0, -900.)
        self.batch = pyglet.graphics.Batch()
        self.tunnel_batch = pyglet.graphics.Batch()
        self.ant_image = pyglet.resource.image('ant.png')
        self.opening_image = pyglet.resource.image('ground.png')
        self.encasing_image = pyglet.resource.image('encasing.png')
        self.ants = []
        self.tunnel_openings = []

        self.space.add_collision_handler(
            constants.ANT_COLLISION_TYPE,
            constants.OPENING_COLLISION_TYPE,
        )
        pyglet.gl.glClearColor(*constants.DEF_BKGDCOLOR)
        pyglet.clock.schedule(self.update)
        self.populate_grid()

    def populate_grid(self):
        rows = self.height / constants.GRID_TILE_LENGTH
        cols = self.width / constants.GRID_TILE_LENGTH
        offset = constants.GRID_TILE_LENGTH / 2
        self.grid = [[0 for x in xrange(cols)] for x in xrange(rows)]
        for row in xrange(rows):
            for col in xrange(cols):
                x_pos = col * constants.GRID_TILE_LENGTH + offset
                y_pos = row * constants.GRID_TILE_LENGTH + offset
                if row == 0 or row == rows or col == 0 or col == cols - 1:
                    self.add_tile('encasing', (row, col),
                                  (x_pos, y_pos), constants.GRID_TILE_LENGTH)
                elif row == 1 and col == 1:
                    self.add_ant((row, col), (x_pos, y_pos))
                else:
                    self.add_tile('opening', (row, col), (x_pos, y_pos), constants.GRID_TILE_LENGTH)

    def add_tile(self, tile_type, grid_pos, body_pos, tile_length):
        """Adds a tile to the grid."""
        if tile_type == 'opening':
            cls = Opening
            image = self.opening_image
        elif tile_type == 'encasing':
            cls = Encasing
            image = self.encasing_image
        (body_x, body_y) = body_pos
        (grid_x, grid_y) = grid_pos
        tile = cls(
            self.tunnel_batch, self.space.static_body,
            image, self.space,
            body_x, body_y, tile_length
        )
        self.grid[grid_x][grid_y] = tile

    def add_ant(self, grid_pos, body_pos):
        """Add an ant to the game."""
        (body_x, body_y) = body_pos
        (grid_x, grid_y) = grid_pos
        ant = Ant(batch=self.batch, img=self.ant_image, space=self.space, x=body_x, y=body_y)
        self.grid[grid_x][grid_y] = ant

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
        for row in self.grid:
            for col in xrange(len(row)):
                elem = row[col]
                if isinstance(elem, Ant):
                    elem.update(dt, self.keys)
        self.space.step(dt)
