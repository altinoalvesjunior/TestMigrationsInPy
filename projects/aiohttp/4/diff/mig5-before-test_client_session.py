import unittest
from aiohttp.client import ClientSession

class TestClientSession(unittest.TestCase):

    def test_init_cookies_with_simple_dict(self):
        session = ClientSession(
            cookies={
                "c1": "cookie1",
                "c2": "cookie2"
            }, loop=self.loop)
        self.assertEqual(set(session.cookies), {'c1', 'c2'})
        self.assertEqual(session.cookies['c1'].value, 'cookie1')
        self.assertEqual(session.cookies['c2'].value, 'cookie2')
        session.close()