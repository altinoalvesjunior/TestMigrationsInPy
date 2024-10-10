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
    def setUp(self):
        self.key = object()
        self.connector = mock.Mock()
        self.request = mock.Mock()
        self.transport = mock.Mock()
        self.protocol = mock.Mock()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)