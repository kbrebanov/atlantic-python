from .utils import AtlanticBase
from .image import AtlanticImage
from .plan import AtlanticPlan
from .server import AtlanticServer

class Atlantic(AtlanticBase):
    def __init__(self, access_key, private_key):
        AtlanticBase.__init__(self, access_key, private_key)
        self.image = AtlanticImage(access_key, private_key)
        self.plan = AtlanticPlan(access_key, private_key)
        self.server = AtlanticServer(access_key, private_key)
