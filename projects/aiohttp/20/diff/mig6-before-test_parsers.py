import unittest
import asyncio
from aiohttp import parsers

class TestStreamParser(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_feed_none_data(self):
        stream = parsers.StreamParser(loop=self.loop)
        stream.feed_data(None)
        self.assertEqual(b'', bytes(stream._buffer))