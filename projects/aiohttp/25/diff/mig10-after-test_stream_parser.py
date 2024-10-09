import pytest
from aiohttp import parsers

def test_set_parser_feed_existing_exc(loop):
    def p(out, buf):
        yield from buf.read(1)
        raise ValueError()
    stream = parsers.StreamParser(loop=loop)
    stream.feed_data(b'line1')
    s = stream.set_parser(p)
    assert isinstance(s.exception(), ValueError)