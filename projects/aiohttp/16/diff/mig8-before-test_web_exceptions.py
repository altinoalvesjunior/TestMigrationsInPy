import unittest
from aiohttp import web

class TestHTTPExceptions(unittest.TestCase):
    def test_override_body_with_binary(self):
        txt = "<html><body>Page not found</body></html>"
        resp = web.HTTPNotFound(body=txt.encode('utf-8'),
                                content_type="text/html")
        self.assertEqual(404, resp.status)
        self.assertEqual(txt.encode('utf-8'), resp.body)
        self.assertEqual(txt, resp.text)
        self.assertEqual("text/html", resp.content_type)
        self.assertIsNone(resp.charset)