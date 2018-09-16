import unittest

from yget.authentication_provider import AuthenticationProvider

from .mock_input_provider import MockInputProvider

class TestAuthenticationProvider(unittest.TestCase):
    def make_authentication_provider(self, mock_input_provider=None):
        if not mock_input_provider:
            mock_input_provider = MockInputProvider(lambda x: "", lambda x: "")

        return AuthenticationProvider(mock_input_provider)

    def test_when_username_is_none_returns_false(self):
        authentication_provider = self.make_authentication_provider()

        output = {}
        result = authentication_provider.request_authentication_parameters(output)

        self.assertDictEqual(output, {})
        self.assertFalse(result)

    def test_when_username_exists_returns_true(self):
        mock_input_provider = MockInputProvider(lambda x: "INPUT", lambda x: "")

        authentication_provider = self.make_authentication_provider(mock_input_provider=mock_input_provider)

        output = {}
        result = authentication_provider.request_authentication_parameters(output)

        self.assertDictEqual(output, {
            "username": "INPUT",
            "password": ""
        })
        self.assertTrue(result)
