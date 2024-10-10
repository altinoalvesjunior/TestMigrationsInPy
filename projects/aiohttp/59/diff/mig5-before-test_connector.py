import asyncio
import unittest
from unittest import mock
from yarl import URL
import aiohttp
from aiohttp.client import ClientRequest
from aiohttp.test_utils import unused_port

class TestHttpClientConnector(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.stop()
        self.loop.run_forever()
        self.loop.close()

    def test_resolver_not_called_with_address_is_ip(self):
        resolver = mock.MagicMock()
        connector = aiohttp.TCPConnector(resolver=resolver, loop=self.loop)

        req = ClientRequest('GET',
                            URL('http://127.0.0.1:{}'.format(unused_port())),
                            loop=self.loop,
                            response_class=mock.Mock())

        with self.assertRaises(OSError):
            self.loop.run_until_complete(connector.connect(req))

        resolver.resolve.assert_not_called()