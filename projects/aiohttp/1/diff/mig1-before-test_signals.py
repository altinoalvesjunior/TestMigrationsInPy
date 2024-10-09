import asyncio
import unittest
from unittest import mock
from aiohttp.multidict import CIMultiDict
from aiohttp.signals import Signal
from aiohttp.web import Application
from aiohttp.web import Request, Response
from aiohttp.protocol import HttpVersion11
from aiohttp.protocol import RawRequestMessage

class TestSignals(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def make_request(self, method, path, headers=CIMultiDict(), app=None):
        message = RawRequestMessage(method, path, HttpVersion11, headers,
                                    False, False)
        return self.request_from_message(message, app)