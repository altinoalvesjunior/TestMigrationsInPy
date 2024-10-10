import unittest
from yarl import URL
from aiohttp.client_reqrep import ClientResponse

class TestClientResponse(unittest.TestCase):

    def test_resp_host(self):
        response = ClientResponse('get', URL('http://del-cl-resp.org'))
        with self.assertWarns(DeprecationWarning):
            self.assertEqual('del-cl-resp.org', response.host)