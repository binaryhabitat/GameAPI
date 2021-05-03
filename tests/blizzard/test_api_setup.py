import unittest

from GameAPI.blizzard.warcraft import WarcraftAPI
from GameAPI.blizzard.helpers import OAuthToken


class TestAPISetup(unittest.TestCase):
    def setUp(self) -> None:
        self.test_valid_client_id = "test_id"
        self.test_valid_client_secret = "test_secret"
        self.test_valid_region = "test_region"

    def test_valid_args_create_class_set(self) -> None:
        api = WarcraftAPI(client_id=self.test_valid_client_id,
                          client_secret=self.test_valid_client_secret,
                          region=self.test_valid_region)
        self.assertEqual(self.test_valid_client_id, api.client_id)
        self.assertEqual(self.test_valid_client_secret, api.client_secret)

    def test_invalid_api_instantiation(self):
        """
        assertRaisesRegex cannot be used, as the actual instantiation fails.

        This unit tests is making sure no one accidentally makes an arg optional in the future.
        """
        try:
            # noinspection PyArgumentList
            WarcraftAPI()
        except TypeError as e:
            self.assertEqual("__init__() missing 3 required positional arguments: "
                             "'client_id', 'client_secret', and 'region'", str(e))
        else:
            raise AssertionError("Exception not encountered.")

    def test_default_oauth_token_is_empty(self):
        api = WarcraftAPI(client_id=self.test_valid_client_id,
                          client_secret=self.test_valid_client_secret,
                          region=self.test_valid_region)
        self.assertIsInstance(api.oauth_token, OAuthToken)
        self.assertEqual("", api.oauth_token.token)


if __name__ == '__main__':
    unittest.main()
