from __future__ import absolute_import

import pyglet

from antfarm.lib.game import Game

pyglet.resource.path = ['static']
pyglet.resource.reindex()

game = Game()
game.add_ant()
game.add_to_tunnel(200, 200)
game.add_to_tunnel(220, 210)

pyglet.app.run()
