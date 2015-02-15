import random

from antfarm.lib import constants


class AI(object):

    def __init__(self):
        self.memory_size = 100
        self.initiate_memory()

    def initiate_memory(self):
        """Initiates the hosts memory."""
        rows = constants.WINDOW_HEIGHT / constants.GRID_TILE_LENGTH
        cols = constants.WINDOW_WIDTH / constants.GRID_TILE_LENGTH
        self.memory = [[None for x in xrange(cols)] for x in xrange(rows)]

    def remember(self, grid_x, grid_y, obj):
        """Remember the position of something."""
        self.memory[grid_x][grid_y] = obj

    def get_grid_position(self):
        """Get the grid position of host."""
        tile_size_x = constants.WINDOW_WIDTH / constants.GRID_TILE_LENGTH
        tile_size_y = constants.WINDOW_HEIGHT / constants.GRID_TILE_LENGTH
        grid_x = tile_size_x / self.host.x
        grid_y = tile_size_y / self.host.y
        return grid_x, grid_y

    def saw(self, obj):
        """Something was seen."""
        grid_x = obj.grid_x
        grid_y = obj.grid_y
        self.remember(grid_x, grid_y, obj)
        self.interact_with(obj)

    def interact_with(self, obj):
        """Interact with objects."""
        if obj.id == 'DIRT':
            obj.dig(self.dig_speed)

    def explore(self, dt):
        """Explore the world."""
        dirs = [constants.UP, constants.DOWN, constants.LEFT, constants.RIGHT]
        self.move(random.choice(dirs), dt)

    def update(self, dt):
        self.explore(dt)
