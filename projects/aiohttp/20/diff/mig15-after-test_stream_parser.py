import pytest
from aiohttp import parsers

def test_set_parser_feed_existing_stop(loop):
    def LinesParser(out, buf):
        try:
            chunk = yield from buf.readuntil(b'\n')
            out.feed_data(chunk, len(chunk))
            chunk = yield from buf.readuntil(b'\n')
            out.feed_data(chunk, len(chunk))
        finally:
            out.feed_eof()
    stream = parsers.StreamParser(loop=loop)
    stream.feed_data(b'line1')
    stream.feed_data(b'\r\nline2\r\ndata')
    s = stream.set_parser(LinesParser)
    assert b'line1\r\nline2\r\n' == b''.join(d for d, _ in s._buffer)
    assert b'data' == bytes(stream._buffer)
    assert stream._parser is None
    assert s._eof