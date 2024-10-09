import pytest
from aiohttp import parsers

def test_unset_parser_stop(loop):
    def p(out, buf):
        try:
            while True:
                yield  # read chunk
        except parsers.EofStream:
            out.feed_eof()
    stream = parsers.StreamParser(loop=loop)
    s = stream.set_parser(p)
    stream.feed_data(b'line1')
    stream.unset_parser()
    assert s._eof