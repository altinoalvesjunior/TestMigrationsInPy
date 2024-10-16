import unittest
from aiohttp.client import ClientSession

class TestClientSession(unittest.TestCase):

    def test_borrow_connector_loop(self):
        conn = self.make_open_connector()
        session = ClientSession(connector=conn)
        self.assertIs(session._loop, self.loop)
        session.close()