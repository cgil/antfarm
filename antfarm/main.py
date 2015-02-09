from __future__ import absolute_import

import pyglet

from antfarm.lib.game import Game

pyglet.resource.path = ['static']
pyglet.resource.reindex()

game = Game()

pyglet.app.run()
