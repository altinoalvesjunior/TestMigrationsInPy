import unittest
from yarl import URL
from aiohttp.client_reqrep import ClientResponse
import aiohttp

class TestClientResponse(unittest.TestCase):

    def test_raise_for_status_4xx(self):
        self.response = ClientResponse('get', URL('http://def-cl-resp.org'))
        self.response.status = 409
        self.response.reason = 'CONFLICT'
        with self.assertRaises(aiohttp.HttpProcessingError) as cm:
            self.response.raise_for_status()
        self.assertEqual(str(cm.exception.code), '409')
        self.assertEqual(str(cm.exception.message), "CONFLICT")