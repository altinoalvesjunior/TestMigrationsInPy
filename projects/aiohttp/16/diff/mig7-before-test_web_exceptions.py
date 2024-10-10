import unittest
from aiohttp import web

class TestHTTPExceptions(unittest.TestCase):
    def test_override_body_with_text(self):
        resp = web.HTTPNotFound(text="Page not found")
        self.assertEqual(404, resp.status)
        self.assertEqual("Page not found".encode('utf-8'), resp.body)
        self.assertEqual("Page not found", resp.text)
        self.assertEqual("text/plain", resp.content_type)
        self.assertEqual("utf-8", resp.charset)