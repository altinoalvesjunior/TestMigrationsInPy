import unittest
from aiohttp import web

class TestHTTPExceptions(unittest.TestCase):
    def test_empty_body_204(self):
        resp = web.HTTPNoContent()
        self.assertIsNone(resp.body)