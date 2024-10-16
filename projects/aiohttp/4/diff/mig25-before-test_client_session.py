import unittest
from aiohttp.client import ClientSession

class TestClientSession(unittest.TestCase):

    def test_double_close(self):
        conn = self.make_open_connector()
        session = ClientSession(loop=self.loop, connector=conn)

        session.close()
        self.assertIsNone(session.connector)
        session.close()
        self.assertTrue(session.closed)
        self.assertTrue(conn.closed)