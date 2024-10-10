import unittest
import asyncio
from aiohttp import parsers

class TestStreamParser(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_exception(self):
        stream = parsers.StreamParser(loop=self.loop)
        self.assertIsNone(stream.exception())
        exc = ValueError()
        stream.set_exception(exc)
        self.assertIs(stream.exception(), exc)