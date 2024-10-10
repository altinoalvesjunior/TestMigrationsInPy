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
    def test_add_signal_handler_not_a_callable(self):
        callback = True
        app = Application(loop=self.loop)
        app.on_response_prepare.append(callback)
        with self.assertRaises(TypeError):
            app.on_response_prepare(None, None)