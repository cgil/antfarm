import pyglet
import pymunk
from pymunk.pyglet_util import draw as pymunk_draw
from pyglet.window import key

from antfarm.lib import constants
from antfarm.lib.ant import Ant
from antfarm.lib.dirt import DIRT
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
        self.dirt_image = pyglet.resource.image('ground.png')
        self.encasing_image = pyglet.resource.image('encasing.png')
        self.ants = []
        self.tunnel_dirts = []

        self.space.add_collision_handler(
            constants.ANT_COLLISION_TYPE,
            constants.DIRT_COLLISION_TYPE,
            pre_solve=self.pre_solve_handler,
        )
        pyglet.gl.glClearColor(*constants.DEF_BKGDCOLOR)
        pyglet.clock.schedule(self.update)
        self.initiate_grid()

    def initiate_grid(self):
        """Initiate the grid."""
        rows = self.height / constants.GRID_TILE_LENGTH
        cols = self.width / constants.GRID_TILE_LENGTH
        offset = constants.GRID_TILE_LENGTH / 2
        self.grid = [[0 for x in xrange(cols)] for x in xrange(rows)]
        for row in xrange(rows):
            for col in xrange(cols):
                x_pos = col * constants.GRID_TILE_LENGTH + offset
                y_pos = row * constants.GRID_TILE_LENGTH + offset
                if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
                    self.add_tile('encasing', (row, col),
                                  (x_pos, y_pos), constants.GRID_TILE_LENGTH)
                elif row == rows - 5 and col == cols / 2:
                    self.add_ant((x_pos, y_pos))
                    self.grid[row][col] = None
                else:
                    self.add_tile('dirt', (row, col), (x_pos, y_pos), constants.GRID_TILE_LENGTH)
        ten_pct_rows = int(rows * 0.1)
        for row in xrange(ten_pct_rows):
            from_top_row = rows - row - 1
            for col in xrange(cols):
                if col == 0 or col == cols - 1:
                    continue
                self.remove(self.grid[from_top_row][col])

    def add_tile(self, tile_type, grid_pos, body_pos, tile_length):
        """Adds a tile to the grid."""
        if tile_type == 'dirt':
            cls = DIRT
            image = self.dirt_image
        elif tile_type == 'encasing':
            cls = Encasing
            image = self.encasing_image
        (body_x, body_y) = body_pos
        (grid_x, grid_y) = grid_pos
        tile = cls(
            self.tunnel_batch, self.space.static_body,
            image, self.space,
            body_x, body_y, tile_length, grid_pos
        )
        self.grid[grid_x][grid_y] = tile

    def pre_solve_handler(self, space, arbiter):
        ant = None
        dirt = None
        for shape in arbiter.shapes:
            if shape.collision_type == constants.DIRT_COLLISION_TYPE:
                dirt = shape.ref
            elif shape.collision_type == constants.ANT_COLLISION_TYPE:
                ant = shape.ref
        ant.saw(dirt)
        return True

    def remove(self, obj):
        """Remove an object from the game."""
        if not obj:
            return
        self.space.remove(obj.shape)
        self.grid[obj.grid_x][obj.grid_y] = None

    def add_ant(self, body_pos):
        """Add an ant to the game."""
        (body_x, body_y) = body_pos
        ant = Ant(batch=self.batch, img=self.ant_image, space=self.space, x=body_x, y=body_y)
        self.ants.append(ant)

    def on_draw(self):
        self.clear()
        pymunk_draw(self.tunnel_dirts, self.tunnel_batch)
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
            self.keys[constants.UP] = False
        elif symbol == key.LEFT:
            self.keys[constants.LEFT] = False
        elif symbol == key.RIGHT:
            self.keys[constants.RIGHT] = False
        elif symbol == key.DOWN:
            self.keys[constants.DOWN] = False

    def update(self, dt):
        for ant in self.ants:
            ant.update(dt, self.keys)

        for row in self.grid:
            for obj in row:
                try:
                    if not obj.is_alive:
                        self.remove(obj)
                except Exception:
                    pass
        self.space.step(dt)
