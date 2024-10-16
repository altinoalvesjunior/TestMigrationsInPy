import unittest
import asyncio
from aiohttp.client import ClientSession
from aiohttp.connector import TCPConnector

class TestClientSession(unittest.TestCase):

    def test_connector_loop(self):
        loop = asyncio.new_event_loop()
        connector = TCPConnector(loop=loop)
        with self.assertRaisesRegex(
                ValueError,
                "loop argument must agree with connector"):
            ClientSession(connector=connector, loop=self.loop)
        connector.close()
        loop.close()