import unittest
import asyncio
from aiohttp import parsers

class TestStreamParser(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_exception_waiter(self):
        stream = parsers.StreamParser(loop=self.loop)
        lines_parser = parsers.LinesParser()
        stream._parser = lines_parser
        buf = stream._output = parsers.FlowControlDataQueue(
            stream, loop=self.loop)
        exc = ValueError()
        stream.set_exception(exc)
        self.assertIs(buf.exception(), exc)