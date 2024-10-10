import unittest
import unittest.mock
import asyncio
from aiohttp import parsers

class TestStreamParser(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_set_parser_unset_prev(self):
        stream = parsers.StreamParser(loop=self.loop)
        lines_parser = parsers.LinesParser()
        stream.set_parser(lines_parser)
        unset = stream.unset_parser = unittest.mock.Mock()
        stream.set_parser(lines_parser)
        self.assertTrue(unset.called)