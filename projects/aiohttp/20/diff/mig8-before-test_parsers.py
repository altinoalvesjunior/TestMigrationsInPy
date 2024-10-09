import unittest
import asyncio
from aiohttp import parsers

class TestStreamParser(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_set_parser_exception(self):
        stream = parsers.StreamParser(loop=self.loop)
        lines_parser = parsers.LinesParser()
        exc = ValueError()
        stream.set_exception(exc)
        s = stream.set_parser(lines_parser)
        self.assertIs(s.exception(), exc)