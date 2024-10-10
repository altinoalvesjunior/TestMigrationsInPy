import asyncio
import unittest
import aiohttp
from aiohttp import helpers, client
from aiohttp.test_utils import run_briefly, unused_port

def test_session_auth_override(self):
    with run_server(self.loop, router=Functional) as httpd:
        session = client.ClientSession(
            loop=self.loop, auth=helpers.BasicAuth("login", "pass"))
        r = self.loop.run_until_complete(
            session.request('get', httpd.url('method', 'get'),
                            auth=helpers.BasicAuth("other_login", "pass")))
        self.assertEqual(r.status, 200)
        content = self.loop.run_until_complete(r.json())
        self.assertIn("Authorization", content['headers'])
        self.assertEqual(content['headers']["Authorization"], "Basic b3RoZXJfbG9naW46cGFzcw==")
        r.close()
        self.loop.run_until_complete(session.close())