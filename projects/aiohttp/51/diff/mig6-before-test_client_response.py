import unittest
from yarl import URL
from aiohttp.client_reqrep import ClientResponse

class TestClientResponse(unittest.TestCase):

    def test_repr_non_ascii_url(self):
        response = ClientResponse('get', URL('http://fake-host.org/\u03bb'))
        self.assertIn(
            "<ClientResponse(http://fake-host.org/%CE%BB) [None None]>",
            repr(response))