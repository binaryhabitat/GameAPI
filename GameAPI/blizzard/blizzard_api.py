from .battlenet import BattleNetAPI
from .diablo3 import Diablo3API
from .hearthstone import HearthstoneAPI
from .warcraft import WarcraftAPI


class BlizzardAPI:
    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 region: str):
        self.battlenet = BattleNetAPI(client_id, client_secret, region)
        self.diablo3 = Diablo3API(client_id, client_secret, region)
        self.hearthstone = HearthstoneAPI(client_id, client_secret, region)
        self.wow = WarcraftAPI(client_id, client_secret, region)
        self.wow_classic = WarcraftAPI(client_id, client_secret, region, classic=True)
