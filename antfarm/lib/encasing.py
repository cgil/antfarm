from __future__ import absolute_import

from antfarm.lib import constants
from antfarm.lib.tile import Tile


class Encasing(Tile):

    def __init__(self, *args, **kwargs):
        super(Encasing, self).__init__(*args, **kwargs)
        self.id = constants.ENCASING_ID
        self.shape.group = constants.ENCASING_GROUP
        self.shape.collision_type = constants.ENCASING_COLLISION_TYPE
