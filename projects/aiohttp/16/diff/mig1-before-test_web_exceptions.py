import unittest
from aiohttp import web

class TestHTTPExceptions(unittest.TestCase):
    def test_all_http_exceptions_exported(self):
        self.assertIn('HTTPException', web.__all__)
        for name in dir(web):
            if name.startswith('_'):
                continue
            obj = getattr(web, name)
            if isinstance(obj, type) and issubclass(obj, web.HTTPException):
                self.assertIn(name, web.__all__)