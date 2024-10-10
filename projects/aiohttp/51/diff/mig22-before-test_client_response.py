import unittest
from yarl import URL
from aiohttp.client_reqrep import ClientResponse

class TestClientResponse(unittest.TestCase):

    def test_raise_for_status_2xx(self):
        self.response = ClientResponse('get', URL('http://def-cl-resp.org'))
        self.response.status = 200
        self.response.reason = 'OK'
        self.response.raise_for_status()  # should not raise