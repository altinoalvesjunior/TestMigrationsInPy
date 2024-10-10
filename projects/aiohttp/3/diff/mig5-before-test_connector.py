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
    def test_release_released(self):
        conn = Connection(
            self.connector, self.key, self.request,
            self.transport, self.protocol, self.loop)
        conn.release()
        self.connector._release.reset_mock()
        conn.release()
        self.assertFalse(self.transport.close.called)
        self.assertIsNone(conn._transport)
        self.assertFalse(self.connector._release.called)
