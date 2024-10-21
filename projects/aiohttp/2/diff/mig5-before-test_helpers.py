import unittest
from aiohttp import helpers

class TestHelpers(unittest.TestCase):

    def test_invalid_formdata_content_type(self):
        form = helpers.FormData()
        invalid_vals = [0, 0.1, {}, [], b'foo']
        for invalid_val in invalid_vals:
            with self.assertRaises(TypeError):
                form.add_field('foo', 'bar', content_type=invalid_val)