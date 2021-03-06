from GameAPI.blizzard.base_api import BaseAPI


class BattleNetAPI(BaseAPI):
    def __init__(self, client_id: str, client_secret: str, region: str):
        super().__init__(client_id, client_secret, region)
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_region = region
