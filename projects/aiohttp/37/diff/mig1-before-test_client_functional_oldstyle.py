import asyncio
import io
import json
import pathlib
import ssl
import unittest
from unittest import mock

from multidict import MultiDict

import aiohttp
from aiohttp import hdrs, web
from aiohttp.errors import FingerprintMismatch

class TestHttpClientFunctional(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.get_event_loop()
        cls.here = pathlib.Path(__file__).parent

    @classmethod
    def tearDownClass(cls):
        cls.loop.close()

    def setUp(self):
        self.ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        self.ssl_ctx.load_cert_chain(
            str(self.here / 'sample.crt'),
            str(self.here / 'sample.key'))
        self.fname = self.here / 'sample.key'

    def test_POST_FILES(self):
        with test_utils.run_server(self.loop, router=Functional) as httpd:
            @asyncio.coroutine
            def handler(request):
                data = yield from request.post()
                assert data['some'].filename == self.fname.name
                with self.fname.open('rb') as f:
                    content1 = f.read()
                content2 = data['some'].file.read()
                assert content1 == content2
                assert data['test'].file.read() == b'data'
                return web.HTTPOk()
            app, client = yield from create_app_and_client()
            app.router.add_post('/', handler)
            with self.fname.open() as f:
                resp = yield from client.post('/', data={'some': f, 'test': b'data'},
                                              chunked=1024,
                                              headers={'Transfer-Encoding': 'chunked'})
                assert 200 == resp.status
                resp.close()