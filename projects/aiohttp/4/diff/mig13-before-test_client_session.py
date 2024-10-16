import unittest
from unittest import mock
from aiohttp.client import ClientSession

class TestClientSession(unittest.TestCase):

    @mock.patch("aiohttp.client.ClientSession._request")
    def test_http_POST(self, patched):
        session, params = self._make_one()
        session.post(
            "http://post.example.com",
            params={"x": 2},
            data="Some_data",
            **params)
        self.assertTrue(patched.called, "`ClientSession._request` not called")
        self.assertEqual(
            list(patched.call_args),
            [("POST", "http://post.example.com",),
             dict(
                params={"x": 2},
                data="Some_data",
                **params)])
        session.close()