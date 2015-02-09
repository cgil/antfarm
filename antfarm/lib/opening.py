from __future__ import absolute_import

from antfarm.lib import constants
from antfarm.lib.tile import Tile


class Opening(Tile):

    def __init__(self, *args, **kwargs):
        super(Opening, self).__init__(*args, **kwargs)
        self.shape.group = constants.OPENING_GROUP
        self.shape.collision_type = constants.OPENING_COLLISION_TYPE
