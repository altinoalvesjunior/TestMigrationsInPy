import unittest
from aiohttp import helpers

class TestHelpers(unittest.TestCase):

    def test_invalid_formdata_params(self):
        with self.assertRaises(TypeError):
            helpers.FormData('asdasf')