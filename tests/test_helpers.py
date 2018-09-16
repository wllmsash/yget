import unittest

from yget.helpers import Helpers

class TestAuthenticationProvider(unittest.TestCase):
    def test_strings_stripped_correctly(self):
        stripped_strings = Helpers.strip_strings([" a ", "b ", " c", "ab\r"])

        self.assertListEqual(stripped_strings, ["a", "b", "c", "ab"])
