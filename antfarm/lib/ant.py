from __future__ import absolute_import

from weakref import proxy

import pyglet
import pymunk

from antfarm.lib.ai import AI
from antfarm.lib import constants


class Ant(pyglet.sprite.Sprite, AI):

    def __init__(self, batch, img, space, x, y):
        img.width = constants.ANT_LENGTH
        img.height = constants.ANT_LENGTH
        img.anchor_x = img.width / 2
        img.anchor_y = img.height / 2
        self.id = constants.ANT_ID
        self.dig_speed = constants.ANT_DIG_SPEED
        self.dx = 20
        self.dy = 20
        self.rotation_speed = 220
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
        AI.__init__(self)

    def rotate(self, to, dt):
        """Rotates to a given angle."""
        initial = self.rotation
        diff = to - initial
        signed_angle = (diff + 180) % 360 - 180
        if signed_angle > 0:
            diff -= 180
            self.rotation += self.rotation_speed * dt
        elif signed_angle < 0:
            self.rotation += -self.rotation_speed * dt

    def move(self, direction, dt):
        """Move in a given direction."""
        if direction == constants.LEFT:
            self.body.position.x -= self.dx * dt
            self.rotate(270, dt)
        elif direction == constants.RIGHT:
            self.body.position.x += self.dx * dt
            self.rotate(90, dt)
        elif direction == constants.UP:
            self.body.position.y += self.dy * dt
            self.rotate(0, dt)
        elif direction == constants.DOWN:
            self.body.position.y -= self.dy * dt
            self.rotate(180, dt)

        self.x = self.body.position.x
        self.y = self.body.position.y

    def update(self, dt, keys):
        for direction in keys:
            if keys[direction]:
                self.move(direction, dt)
        AI.update(self, dt)
