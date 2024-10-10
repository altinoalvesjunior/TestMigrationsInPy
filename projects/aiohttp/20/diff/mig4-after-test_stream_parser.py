import pytest
from aiohttp import parsers

@pytest.fixture
def lines_parser():
    return parsers.LinesParser()

def test_exception_waiter(loop, lines_parser):
    stream = parsers.StreamParser(loop=loop)
    stream._parser = lines_parser
    buf = stream._output = parsers.FlowControlDataQueue(
        stream, loop=loop)
    exc = ValueError()
    stream.set_exception(exc)
    assert buf.exception() is exc