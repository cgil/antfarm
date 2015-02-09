from __future__ import absolute_import

from weakref import proxy

import pyglet
import pymunk

from antfarm.lib import constants


class Ant(pyglet.sprite.Sprite):

    def __init__(self, batch, img, space, x, y):
        img.width = constants.ANT_LENGTH
        img.height = constants.ANT_LENGTH
        img.anchor_x = img.width / 2
        img.anchor_y = img.height / 2
        self.dig_speed = constants.ANT_DIG_SPEED
        self.dx = 20
        self.dy = 20
        self.mass = 10
        self.inertia = pymunk.moment_for_circle(self.mass, img.width / 2, 0.0, (0, 0))
        self.body = pymunk.Body(self.mass, self.inertia)
        self.shape = pymunk.Circle(self.body, img.width / 2, (0, 0))
        self.shape.collision_type = constants.ANT_COLLISION_TYPE
        self.shape.ref = proxy(self)
        self.body.position = x, y
        space.add(self.body, self.shape)
        super(Ant, self).__init__(
            img, x=self.body.position.x, y=self.body.position.y, batch=batch)

    def update(self, dt, keys):
        if keys.get('left', None):
            self.body.position.x -= self.dx * dt
        if keys.get('right', None):
            self.body.position.x += self.dx * dt
        if keys.get('up', None):
            self.body.position.y += self.dy * dt
        if keys.get('down', None):
            self.body.position.y -= self.dy * dt

        self.x = self.body.position.x
        self.y = self.body.position.y
