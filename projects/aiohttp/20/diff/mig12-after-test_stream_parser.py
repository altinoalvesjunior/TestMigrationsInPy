import pytest
from aiohttp import parsers

def test_set_parser_feed_existing_eof_exc(loop):
    def p(out, buf):
        try:
            while True:
                yield  # read chunk
        except parsers.EofStream:
            raise ValueError()
    stream = parsers.StreamParser(loop=loop)
    stream.feed_data(b'line1')
    stream.feed_eof()
    s = stream.set_parser(p)
    assert isinstance(s.exception(), ValueError)