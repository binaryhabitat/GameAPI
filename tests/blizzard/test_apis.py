"""
This is a horrible, horrible, horrible test file, it achieves what is desired... but, if you can improve it, please do.

The goal of these tests is the following
    - Call every API method, without having one test per one method
    - Call it with valid type arguments. An int for an int, a string for a string.
    - Check that the URL that would have been requested is constructed in a way we would expect.
"""

import re
import typing
import unittest

import httpx
from mock import patch

from GameAPI.blizzard.diablo3 import Diablo3API
from GameAPI.blizzard.warcraft import WarcraftAPI
from GameAPI.blizzard.hearthstone import HearthstoneAPI


class TestAPIResources(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_response = httpx.Response(status_code=99999)

    @staticmethod
    def get_test_args_for_func(func: any) -> dict:
        params = typing.get_type_hints(func)

        assert ('return' in params)
        del params['return']

        args = {}

        for param in params:
            if params[param] is int:
                val = 0
            elif params[param] is str:
                val = "A"
            elif params[param] is bool:
                val = False
            else:
                val = None

            args[param] = val

        return args

    @patch('GameAPI.blizzard.base_api.BaseAPI._refresh_token')
    @patch('GameAPI.blizzard.base_api.BaseAPI._process_httpx_response', side_effect=lambda x: x)  # noop
    def test_hearthstone_apis(self, _, __):
        hearthstone_api = HearthstoneAPI(client_id="test_id", client_secret="test_secret", region="us")

        functions = [api for api in dir(HearthstoneAPI) if not api.startswith('_') and "request" not in api]

        for func in functions:
            # Get a pointer to the function in the instantiated APIs.
            fn = getattr(hearthstone_api, func)

            # Construct type appropriate arguments for the function
            args = self.get_test_args_for_func(fn)

            with patch('httpx.get', return_value=self.mock_response) as mock_get:
                try:
                    print(f"Calling '{fn.__name__}' with {args}")  # TODO: Log.
                    # Call the function with the args constructed previously
                    resp = fn(**args)
                    print(f"URL {mock_get.mock_calls[0].args[0]}")  # TODO: Log.
                except NotImplementedError as ex:
                    # Some APIs are not implemented, that is fine.
                    continue

                # Make sure we are mocking and not really calling out to the web.
                self.assertEqual(99999, resp.status_code)

                url = mock_get.mock_calls[0][1][0]

                match = re.search(r"https://(.*).api.blizzard.com.*", url)
                # Group 1: Region being queried eg. "us" in us.api.blizzard.com

                # Correct API region?
                self.assertEqual("us", match.group(1))

                # Make sure there's no space in the URL
                self.assertNotIn(" ", match.group(0))

    @patch('GameAPI.blizzard.base_api.BaseAPI._refresh_token')
    @patch('GameAPI.blizzard.base_api.BaseAPI._process_httpx_response', side_effect=lambda x: x)  # noop
    def test_diablo3_apis(self, _, __):
        diablo3_api = Diablo3API(client_id="test_id", client_secret="test_secret", region="us")

        functions = [api for api in dir(Diablo3API) if not api.startswith('_') and "request" not in api]

        for func in functions:
            # Get a pointer to the function in the instantiated APIs.
            fn = getattr(diablo3_api, func)

            # Construct type appropriate arguments for the function
            args = self.get_test_args_for_func(fn)

            with patch('httpx.get', return_value=self.mock_response) as mock_get:
                try:
                    print(f"Calling '{fn.__name__}' with {args}")  # TODO: Log.
                    # Call the function with the args constructed previously
                    resp = fn(**args)
                    print(f"URL {mock_get.mock_calls[0].args[0]}")  # TODO: Log.
                except NotImplementedError as ex:
                    # Some APIs are not implemented, that is fine.
                    continue

                # Make sure we are mocking and not really calling out to the web.
                self.assertEqual(99999, resp.status_code)

                url = mock_get.mock_calls[0][1][0]

                match = re.search(r"https://(.*).api.blizzard.com.*", url)
                # Group 1: Region being queried eg. "us" in us.api.blizzard.com

                # Correct API region?
                self.assertEqual("us", match.group(1))

                # Make sure there's no space in the URL
                self.assertNotIn(" ", match.group(0))

    @patch('GameAPI.blizzard.base_api.BaseAPI._refresh_token')
    @patch('GameAPI.blizzard.base_api.BaseAPI._process_httpx_response', side_effect=lambda x: x)  # noop
    def test_warcraft_apis(self, _, __):
        warcraft_api = WarcraftAPI(client_id="test_id", client_secret="test_secret", region="us")

        functions = [api for api in dir(WarcraftAPI) if not api.startswith('_') and "request" not in api]

        for func in functions:
            # Get a pointer to the function in the instantiated APIs.
            fn = getattr(warcraft_api, func)

            # Construct type appropriate arguments for the function
            args = self.get_test_args_for_func(fn)

            with patch('httpx.get', return_value=self.mock_response) as mock_get:
                try:
                    print(f"Calling '{fn.__name__}' with {args}")  # TODO: Log.
                    # Call the function with the args constructed previously
                    resp = fn(**args)
                    print(f"URL {mock_get.mock_calls[0].args[0]}")  # TODO: Log.
                except NotImplementedError as ex:
                    # Some APIs are not implemented, that is fine.
                    continue

                # Make sure we are mocking and not really calling out to the web.
                self.assertEqual(99999, resp.status_code)

                url = mock_get.mock_calls[0][1][0]

                match = re.search(r"https://(.*).api.blizzard.com.*", url)
                # Group 1: Region being queried eg. "us" in us.api.blizzard.com

                params = mock_get.mock_calls[0][2]['params']

                # Correct API region?
                self.assertEqual("us", match.group(1))

                # Correct namespace region?
                self.assertTrue("us" in params['namespace'])

                # Did API region match namespace region?
                self.assertTrue(match.group(1) in params['namespace'])

                # Valid namespaces are dynamic, static, and profile
                self.assertTrue(params['namespace'] in ("dynamic-us", "static-us", "profile-us"))

                # Make sure there's no space in the URL
                self.assertNotIn(" ", match.group(0))


if __name__ == '__main__':
    unittest.main()
