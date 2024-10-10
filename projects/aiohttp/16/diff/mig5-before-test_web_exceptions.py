import unittest
from aiohttp import web

class TestHTTPExceptions(unittest.TestCase):
    def test_HTTPFound_empty_location(self):
        with self.assertRaises(ValueError):
            web.HTTPFound(location='')
        with self.assertRaises(ValueError):
            web.HTTPFound(location=None)