import unittest
from aiohttp import helpers

class TestHelpers(unittest.TestCase):

    def test_invalid_formdata_content_transfer_encoding(self):
        form = helpers.FormData()
        invalid_vals = [0, 0.1, {}, [], b'foo']
        for invalid_val in invalid_vals:
            with self.assertRaises(TypeError):
                form.add_field('foo',
                               'bar',
                               content_transfer_encoding=invalid_val)