import unittest
from aiohttp.client import ClientSession

class TestClientSession(unittest.TestCase):

    def test_closed(self):
        session = ClientSession(loop=self.loop)
        self.assertFalse(session.closed)
        session.close()
        self.assertTrue(session.closed)