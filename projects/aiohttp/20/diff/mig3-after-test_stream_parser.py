import pytest
from aiohttp import parsers

def test_exception_connection_error(loop):
    stream = parsers.StreamParser(loop=loop)
    assert stream.exception() is None
    exc = ConnectionError()
    stream.set_exception(exc)
    assert stream.exception() is not exc
    assert isinstance(stream.exception(), RuntimeError)
    assert stream.exception().__cause__ is exc
    assert stream.exception().__context__ is exc