import unittest
from aiohttp.client import ClientSession

class TestClientSession(unittest.TestCase):

    def test_detach(self):
        session = ClientSession(loop=self.loop)
        conn = session.connector
        self.assertFalse(conn.closed)
        session.detach()
        self.assertIsNone(session.connector)
        self.assertTrue(session.closed)
        self.assertFalse(conn.closed)
        conn.close()