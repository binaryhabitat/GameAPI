import json

import httpx

from .errors import BlizzardAPIException, BlizzardAPIQuotaException
from .helpers import OAuthToken
from .helpers import datetime_in_n_seconds


class BaseAPI:
    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 region: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_region = region
        self.oauth_token = OAuthToken()

    @staticmethod
    def _process_httpx_response(response: httpx.Response) -> dict:
        if response.status_code not in (200, 429):  # OK, Too Many Requests
            raise BlizzardAPIException(f"Error. Status: {response.status_code}, URL: {response.url}")
        elif response.status_code == 429:  # Too Many Requests
            raise BlizzardAPIQuotaException()

        try:
            # Attempt to json loads the data, this is done blindly
            data = json.loads(response.content)
        except json.JSONDecodeError as ex:
            raise BlizzardAPIException(f"Invalid JSON returned from Blizzard. Exception: {ex}, URL: {response.url}")

        return data

    def _refresh_token(self) -> None:
        # TODO: Log.

        # KR and TW OAuth requests have been merged in APAC.
        # See: https://develop.battle.net/documentation/guides/using-oauth
        region = self.api_region if self.api_region.lower() in ('us', 'eu') else 'apac'

        request = f'https://{region}.battle.net/oauth/token?grant_type=client_credentials' \
                  f'&client_id={self.client_id}' \
                  f'&client_secret={self.client_secret}'

        # Execute the POST request
        response = httpx.post(request)

        # Process the response
        data = self._process_httpx_response(response)

        try:
            # Update the cached token, with the newly received one
            self.oauth_token = OAuthToken(data['access_token'], datetime_in_n_seconds(data['expires_in']))
        except KeyError as ex:
            raise BlizzardAPIException(f"Invalid JSON returned from Blizzard. Exception: {ex}, URL: {request}")

    def request(self, resource: str, parameters: dict = {}) -> dict:
        if not self.oauth_token.token_valid() or not self.oauth_token:
            self._refresh_token()

        # The Base URL for all API requests to Blizzard
        base_url = f"https://{self.api_region}.api.blizzard.com"

        # Add access_token to parameters
        parameters['access_token'] = self.oauth_token.token

        # Construct the final URL to be queried
        request = f"{base_url}{resource}"

        # Execute the GET request
        try:
            response = httpx.get(request, params=parameters)
        except httpx.ReadError as ex:
            # TODO: Log
            raise BlizzardAPIException(f"Exception raised by GET. Exception: {ex}, URL: {request}")

        # Return the response after processing
        return self._process_httpx_response(response)
