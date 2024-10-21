import unittest
from aiohttp import helpers

class TestHelpers(unittest.TestCase):

    def test_invalid_formdata_params2(self):
        with self.assertRaises(TypeError):
            helpers.FormData('as')  # 2-char str is not allowed