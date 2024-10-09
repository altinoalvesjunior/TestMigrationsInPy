import unittest
import asyncio
from aiohttp import parsers

class TestStreamParser(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_exception_connection_error(self):
        stream = parsers.StreamParser(loop=self.loop)
        self.assertIsNone(stream.exception())
        exc = ConnectionError()
        stream.set_exception(exc)
        self.assertIsNot(stream.exception(), exc)
        self.assertIsInstance(stream.exception(), RuntimeError)
        self.assertIs(stream.exception().__cause__, exc)
        self.assertIs(stream.exception().__context__, exc)