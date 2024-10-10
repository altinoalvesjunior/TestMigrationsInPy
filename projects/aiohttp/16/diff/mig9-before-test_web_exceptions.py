import unittest
from aiohttp import web

class TestHTTPExceptions(unittest.TestCase):
    def test_default_body(self):
        resp = web.HTTPOk()
        self.assertEqual(b'200: OK', resp.body)