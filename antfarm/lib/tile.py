from __future__ import absolute_import

import pyglet
import pymunk

from antfarm.lib import constants


class Tile(pyglet.sprite.Sprite):

    def __init__(self, batch, body, img, space, x, y, length):
        img.width = length
        img.height = length
        img.anchor_x = img.width / 2
        img.anchor_y = img.height / 2
        self.shape = pymunk.Circle(body, img.width / 2, (x, y))
        self.shape.color = (255, 0, 0)
        self.shape.group = constants.DEFAULT_GROUP
        self.shape.collision_type = constants.DEFAULT_COLLISION_TYPE
        space.add(self.shape)
        super(Tile, self).__init__(img, x=x, y=y, batch=batch)
