import unittest
from aiohttp.client import ClientSession

class TestClientSession(unittest.TestCase):

    def test_context_manager(self):
        conn = self.make_open_connector()
        with ClientSession(loop=self.loop, connector=conn) as session:
            pass

        self.assertTrue(session.closed)