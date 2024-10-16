import unittest
from aiohttp.client import ClientSession
from aiohttp.connector import TCPConnector

class TestClientSession(unittest.TestCase):

    def test_connector(self):
        connector = TCPConnector(loop=self.loop)
        session = ClientSession(connector=connector, loop=self.loop)
        self.assertIs(session.connector, connector)
        session.close()