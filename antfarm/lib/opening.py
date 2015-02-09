from __future__ import absolute_import

import pyglet
import pymunk

from antfarm.lib import constants


class Opening(pyglet.sprite.Sprite):

    def __init__(self, batch, body, img, space, x=200, y=200):
        img.width = 20
        img.height = 20
        img.anchor_x = img.width / 2
        img.anchor_y = img.height / 2
        self.shape = pymunk.Circle(body, img.width / 2, (x, y))
        self.shape.color = (255, 0, 0)
        self.shape.group = 1
        self.shape.collision_type = constants.OPENING_COLLISION_TYPE
        space.add(self.shape)
        super(Opening, self).__init__(img, x=x, y=y, batch=batch)
