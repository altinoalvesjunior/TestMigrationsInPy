import unittest
from unittest import mock
from aiohttp.client import ClientSession

class TestClientSession(unittest.TestCase):

    @mock.patch("aiohttp.client.ClientSession._request")
    def test_http_PATCH(self, patched):
        session, params = self._make_one()
        session.patch(
            "http://patch.example.com",
            params={"x": 2},
            data="Some_data",
            **params)
        self.assertTrue(patched.called, "`ClientSession._request` not called")
        self.assertEqual(
            list(patched.call_args),
            [("PATCH", "http://patch.example.com",),
             dict(
                params={"x": 2},
                data="Some_data",
                **params)])
        session.close()