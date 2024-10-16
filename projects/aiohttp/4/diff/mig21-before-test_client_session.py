import unittest
from aiohttp.client import ClientSession

class TestClientSession(unittest.TestCase):

    def test_cookies_are_readonly(self):
        session = ClientSession(loop=self.loop)
        with self.assertRaises(AttributeError):
            session.cookies = 123
        session.close()