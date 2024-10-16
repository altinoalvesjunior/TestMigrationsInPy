import unittest
from unittest import mock
from aiohttp.client import ClientSession

class TestClientSession(unittest.TestCase):

    @mock.patch("aiohttp.client.ClientSession._request")
    def test_http_PUT(self, patched):
        session, params = self._make_one()
        session.put(
            "http://put.example.com",
            params={"x": 2},
            data="Some_data",
            **params)
        self.assertTrue(patched.called, "`ClientSession._request` not called")
        self.assertEqual(
            list(patched.call_args),
            [("PUT", "http://put.example.com",),
             dict(
                 params={"x": 2},
                 data="Some_data",
                 **params)])
        session.close()