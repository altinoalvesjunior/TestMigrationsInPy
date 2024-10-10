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
    def test_close(self):
        conn = Connection(
            self.connector, self.key, self.request,
            self.transport, self.protocol, self.loop)
        self.assertFalse(conn.closed)
        conn.close()
        self.assertIsNone(conn._transport)
        self.connector._release.assert_called_with(
            self.key, self.request, self.transport, self.protocol,
            should_close=True)
        self.assertTrue(conn.closed)