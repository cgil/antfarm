from __future__ import absolute_import

from antfarm.lib import constants
from antfarm.lib.tile import Tile


class DIRT(Tile):

    def __init__(self, *args, **kwargs):
        super(DIRT, self).__init__(*args, **kwargs)
        self.id = constants.DIRT_ID
        self.shape.group = constants.DIRT_GROUP
        self.shape.collision_type = constants.DIRT_COLLISION_TYPE
        self.hp = constants.DIRT_HP

    def dig(self, dug_amount=None):
        """Dig into the dirt, remove the tile if its been dug out."""
        if self.hp > 0:
            self.hp = max(self.hp - dug_amount, 0)
        if self.hp == 0:
            self.is_alive = False
