import unittest
import asyncio
from unittest import mock
from aiohttp.client import ClientSession

class TestClientSession(unittest.TestCase):

    def test_reraise_os_error(self):
        @asyncio.coroutine
        def go():
            err = OSError(1, "permission error")
            req = mock.Mock()
            req_factory = mock.Mock(return_value=req)
            req.send = mock.Mock(side_effect=err)
            session = ClientSession(loop=self.loop, request_class=req_factory)
            @asyncio.coroutine
            def create_connection(req):
                # return self.transport, self.protocol
                return mock.Mock(), mock.Mock()
            session._connector._create_connection = create_connection
            with self.assertRaises(aiohttp.ClientOSError) as ctx:
                yield from session.request('get', 'http://example.com')
            e = ctx.exception
            self.assertEqual(e.errno, err.errno)
            self.assertEqual(e.strerror, err.strerror)
        self.loop.run_until_complete(go())