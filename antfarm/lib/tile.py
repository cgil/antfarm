from __future__ import absolute_import

from weakref import proxy

import pyglet
import pymunk

from antfarm.lib import constants


class Tile(pyglet.sprite.Sprite):

    def __init__(self, batch, body, img, space, x, y, length, grid_pos):
        img.width = length
        img.height = length
        img.anchor_x = img.width / 2
        img.anchor_y = img.height / 2
        (self.grid_x, self.grid_y) = grid_pos
        self.id = constants.TILE_ID
        self.is_alive = True
        self.shape = pymunk.Circle(body, img.width / 2, (x, y))
        self.shape.color = (255, 0, 0)
        self.shape.group = constants.DEFAULT_GROUP
        self.shape.collision_type = constants.DEFAULT_COLLISION_TYPE
        self.shape.ref = proxy(self)
        space.add(self.shape)
        super(Tile, self).__init__(img, x=x, y=y, batch=batch)

    def dig(self):
        """Dig out the tile."""
        pass
