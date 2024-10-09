import unittest
import asyncio
from aiohttp import parsers

class TestStreamParser(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_at_eof(self):
        proto = parsers.StreamParser(loop=self.loop)
        self.assertFalse(proto.at_eof())
        proto.feed_eof()
        self.assertTrue(proto.at_eof())