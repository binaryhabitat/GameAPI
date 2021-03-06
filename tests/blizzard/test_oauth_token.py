import unittest
from datetime import datetime, timedelta

import httpx
from mock import patch

from GameAPI.blizzard.errors import BlizzardAPIException, BlizzardAPIQuotaException
from GameAPI.blizzard.helpers import OAuthToken
from GameAPI.blizzard.base_api import BaseAPI


class TestOAuthToken(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_response = httpx.Response(status_code=200)
        self.mock_response._content = '{"access_token":"mock_token","expires_in":100}'
        self.api = BaseAPI(client_id="test_id", client_secret="test_secret", region="us")

    @patch('httpx.get')
    @patch('GameAPI.blizzard.base_api.BaseAPI._process_httpx_response')
    def test_request_with_missing_token_triggers_refresh(self, _, __):
        with patch('GameAPI.blizzard.base_api.BaseAPI._refresh_token') as mock_refresh_func:
            self.api.request("test", parameters={'namespace': 'test'})
            mock_refresh_func.assert_called_once()

    @patch('httpx.get')
    @patch('GameAPI.blizzard.base_api.BaseAPI._process_httpx_response')
    def test_request_with_valid_token_does_not_refresh(self, _, __):
        valid_oauth = OAuthToken("", expiry=datetime.now() + timedelta(1))
        self.api.oauth_token = valid_oauth

        with patch('GameAPI.blizzard.base_api.BaseAPI._refresh_token') as mock_refresh_func:
            self.api.request("test", parameters={'namespace': 'test'})
            mock_refresh_func.assert_not_called()

    def test_refresh_token_queries_correct_region(self):
        for region in "eu", "us", "apac":
            api = BaseAPI(client_id="test_id", client_secret="test_secret", region=region)
            with patch('httpx.post', return_value=self.mock_response) as mock_post:
                api._refresh_token()
                mock_post.assert_called_once_with("https://{}.battle.net/oauth/token?grant_type=client_credentials"
                                                  "&client_id=test_id"
                                                  "&client_secret=test_secret".format(region))

    def test_refresh_token_raises_on_error_code(self):
        url = "https://www.example.com"

        for error in 501, 404, 100:
            mock_request = httpx.Request(method="GET", url=url)

            with patch('httpx.post', return_value=httpx.Response(status_code=error, request=mock_request)):
                with self.assertRaises(BlizzardAPIException) as ex:
                    self.api._refresh_token()
                self.assertEqual(f'Error. Status: {error}, URL: {url}', str(ex.exception))

    def test_refresh_token_raises_quota_error_on_429(self):
        with patch('httpx.post', return_value=httpx.Response(status_code=429)):
            with self.assertRaises(BlizzardAPIQuotaException):
                self.api._refresh_token()

    if __name__ == '__main__':
        unittest.main()
