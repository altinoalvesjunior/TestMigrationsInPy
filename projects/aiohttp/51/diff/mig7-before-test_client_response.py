import unittest
from yarl import URL
from aiohttp.client_reqrep import ClientResponse

class TestClientResponse(unittest.TestCase):

    def test_repr_non_ascii_reason(self):
        response = ClientResponse('get', URL('http://fake-host.org/path'))
        response.reason = '\u03bb'
        self.assertIn(
            "<ClientResponse(http://fake-host.org/path) [None \\u03bb]>",
            repr(response))