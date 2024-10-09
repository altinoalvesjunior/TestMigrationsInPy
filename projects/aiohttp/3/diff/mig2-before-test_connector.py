import asyncio
import http.cookies
import gc
import socket
import unittest
import ssl
import tempfile
import shutil
import os.path
from unittest import mock

import aiohttp
from aiohttp import web
from aiohttp import client
from aiohttp.client import ClientResponse, ClientRequest
from aiohttp.connector import Connection


class TestHttpConnection(unittest.TestCase):    
    def test_del(self):
        conn = Connection(
            self.connector, self.key, self.request,
            self.transport, self.protocol, self.loop)
        exc_handler = unittest.mock.Mock()
        self.loop.set_exception_handler(exc_handler)
        with self.assertWarns(ResourceWarning):
            del conn
            gc.collect()
        self.connector._release.assert_called_with(self.key,
                                                   self.request,
                                                   self.transport,
                                                   self.protocol,
                                                   should_close=True)
        msg = {'client_connection': unittest.mock.ANY,  # conn was deleted
               'message': 'Unclosed connection'}
        if self.loop.get_debug():
            msg['source_traceback'] = unittest.mock.ANY
        exc_handler.assert_called_with(self.loop, msg)