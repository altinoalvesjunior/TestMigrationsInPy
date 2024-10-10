import unittest
import asyncio
from aiohttp import parsers

class TestStreamParser(unittest.TestCase):
    DATA = b'line1\nline2\nline3\n'

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_feed_data(self):
        stream = parsers.StreamParser(loop=self.loop)
        stream.feed_data(self.DATA)
        self.assertEqual(self.DATA, bytes(stream._buffer))