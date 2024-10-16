import unittest
from unittest import mock
from aiohttp.client import ClientSession

class TestClientSession(unittest.TestCase):

    @mock.patch("aiohttp.client.ClientSession._request")
    def test_http_OPTIONS(self, patched):
        session, params = self._make_one()
        session.options(
            "http://opt.example.com",
            params={"x": 2},
            **params)
        self.assertTrue(patched.called, "`ClientSession._request` not called")
        self.assertEqual(
            list(patched.call_args),
            [("OPTIONS", "http://opt.example.com",),
             dict(
                params={"x": 2},
                allow_redirects=True,
                **params)])
        session.close()