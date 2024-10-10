import asyncio
import unittest
import aiohttp
from aiohttp import helpers, client
from aiohttp.test_utils import run_briefly, unused_port

def test_session_auth_header_conflict(self):
    with run_server(self.loop, router=Functional) as httpd:
        session = client.ClientSession(
            loop=self.loop, auth=helpers.BasicAuth("login", "pass"))
        headers = {'Authorization': "Basic b3RoZXJfbG9naW46cGFzcw=="}
        with self.assertRaises(ValueError):
            self.loop.run_until_complete(
                session.request('get', httpd.url('method', 'get'),
                                headers=headers))
        self.loop.run_until_complete(session.close())