import unittest
from aiohttp.client import ClientSession

class TestClientSession(unittest.TestCase):

    def test_close_flag_for_closed_connector(self):
        session = ClientSession(loop=self.loop)
        conn = session.connector
        self.assertFalse(session.closed)
        conn.close()
        self.assertTrue(session.closed)