import unittest
from unittest import mock
from aiohttp.client import ClientSession

class TestClientSession(unittest.TestCase):

    @mock.patch("aiohttp.client.ClientSession._request")
    def test_http_GET(self, patched):
        session, params = self._make_one()
        session.get(
            "http://test.example.com",
            params={"x": 1},
            **params)
        self.assertTrue(patched.called, "`ClientSession._request` not called")
        self.assertEqual(
            list(patched.call_args),
            [("GET", "http://test.example.com",),
             dict(
                 params={"x": 1},
                 allow_redirects=True,
                 **params)])
        session.close()