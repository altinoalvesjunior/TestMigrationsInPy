import pytest
from aiohttp import parsers

def test_exception(loop):
    stream = parsers.StreamParser(loop=loop)
    assert stream.exception() is None
    exc = ValueError()
    stream.set_exception(exc)
    assert stream.exception() is exc